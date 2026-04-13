from flask import request, jsonify
from application.models import User, Student, Company, Drive, Application, Interview
from application.database import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import app
from sqlalchemy import or_
from application.utils import get_cache, set_cache

@app.route('/api/student/interviews', methods=['GET'])
@jwt_required()
def get_student_interviews():
    identity = get_jwt_identity()
    user_id = identity["id"]
    user = User.query.get(user_id)
    if not user or user.type != 'student':
        return jsonify({"message": "Unauthorized"}), 403

    student = Student.query.filter_by(user_id=user_id).first()
    if not student:
        return jsonify([]), 200

    # Get all applications for the student
    applications = Application.query.filter_by(student_id=student.id).all()
    app_ids = [app.id for app in applications]

    if not app_ids:
        return jsonify([]), 200

    # Get all interviews for those applications
    interviews = Interview.query.filter(Interview.application_id.in_(app_ids)).order_by(Interview.scheduled_at.asc()).all()

    output = []
    for interview in interviews:
        output.append({
            "id": interview.id,
            "drive_title": interview.application.drive.title,
            "drive_id": interview.application.drive_id,
            "company_name": interview.application.drive.company.name,
            "company_logo": interview.application.drive.company.logo,
            "scheduled_at": interview.scheduled_at.isoformat(),
            "mode": interview.mode,
            "location": interview.location,
            "meeting_link": interview.meeting_link,
            "status": interview.application.status
        })

    return jsonify(output), 200


@app.route('/api/student/stats', methods=['GET'])
@jwt_required()
def get_student_stats():
    identity = get_jwt_identity()
    user_id = identity["id"]
    user = User.query.get(user_id)
    if not user or user.type != 'student':
        return jsonify({"message": "Unauthorized"}), 403

    cache_key = f"student:stats:{user_id}"
    cached_data = get_cache(cache_key)
    if cached_data:
        print(f"CACHE HIT: {cache_key}")
        return jsonify(cached_data)

    print(f"CACHE MISS: {cache_key}")
    student = Student.query.filter_by(user_id=user_id).first()
    
    active_drives_count = Drive.query.filter_by(status='Active').count()
    active_recruiters_count = Company.query.filter_by(approved=True, isBlacklisted=False).count()
    
    applications_count = 0
    shortlisted_count = 0
    offers_received_count = 0
    interviews_count = 0

    if student:
        applications_count = Application.query.filter_by(student_id=student.id).count()
        shortlisted_count = Application.query.filter_by(student_id=student.id, status='shortlisted').count()
        offers_received_count = Application.query.filter(
            Application.student_id == student.id,
            Application.status.in_(['offered', 'selected', 'hired', 'placed'])
        ).count()
        
        # Count interviews
        app_ids = [app.id for app in Application.query.filter_by(student_id=student.id).all()]
        if app_ids:
            interviews_count = Interview.query.filter(Interview.application_id.in_(app_ids)).count()

    result = {
        "active_drives": active_drives_count,
        "active_recruiters": active_recruiters_count,
        "shortlisted": shortlisted_count,
        "interviews": interviews_count,
        "offers_received": offers_received_count,
        "applied_at": applications_count
    }
    
    set_cache(cache_key, result, expiry=60)
    return jsonify(result)


@app.route('/api/student/active-drives', methods=['GET'])
@jwt_required()
def get_active_drives():
    identity = get_jwt_identity()
    user_id = identity["id"]
    user = User.query.get(user_id)

    if not user or user.type != 'student':
        return {"message": "Unauthorized"}, 403

    search = request.args.get('search', '')
    
    cache_key = f"student:drives:{user_id}:{search}"
    cached_data = get_cache(cache_key)
    if cached_data:
        print(f"CACHE HIT: {cache_key}")
        return jsonify(cached_data)

    print(f"CACHE MISS: {cache_key}")
    query = Drive.query.join(Company).filter(Drive.status == 'Active')

    if search:
        query = query.filter(
            or_(
                Drive.title.ilike(f'%{search}%'),
                Company.name.ilike(f'%{search}%'),
                Drive.location.ilike(f'%{search}%')
            )
        )

    drives = query.all()

    student = Student.query.filter_by(user_id=user_id).first()
    applied_drive_ids = []
    if student:
        applied_drive_ids = [app.drive_id for app in Application.query.filter_by(student_id=student.id).all()]

    if not drives:
        return {"message": "No active drives found"}, 404

    result = [
        {
            "id": d.id,
            "title": d.title,
            "company_name": d.company.name,
            "company_logo": d.company.logo,
            "company_id": d.company_id,
            "location": d.location,
            "workMode": d.workMode,
            "status": d.status,
            "payScale": d.payScale,
            "positions": d.positions,
            "deadline": d.deadline.isoformat() if d.deadline else None,
            "created_at": d.created_at.isoformat() if d.created_at else None,
            "hasApplied": d.id in applied_drive_ids
        } for d in drives
    ]

    set_cache(cache_key, result, expiry=60)
    return jsonify(result)


# Details of a specific drive
@app.route('/api/student/drive-details/<int:drive_id>', methods=['GET'])
@jwt_required()
def get_drive_details(drive_id):

    identity = get_jwt_identity()
    user_id = identity["id"]

    user = User.query.get(user_id)

    if not user or user.type != 'student':
        return {"message": "Unauthorized"}, 403

    drive = Drive.query.get(drive_id)

    if not drive:
        return {"message": "Drive not found"}, 404

    student = Student.query.filter_by(user_id=user_id).first()
    has_applied = False
    if student:
        has_applied = Application.query.filter_by(student_id=student.id, drive_id=drive_id).first() is not None

    # Students can see the drive if it is 'Active' OR if they have already applied to it
    if drive.status != "Active" and not has_applied:
        return {"message": "Drive is inactive"}, 404

    return jsonify({
        "id": drive.id,
        "title": drive.title,
        "company_name": drive.company.name,
        "company_id": drive.company_id,
        "company_logo": drive.company.logo,
        "description": drive.description,
        "eligibility": drive.eligibility,
        "batch": drive.batch,
        "branches": drive.branches,
        "deadline": drive.deadline.isoformat() if drive.deadline else None,
        "skillsRequired": drive.skillsRequired,
        "payScale": drive.payScale,
        "location": drive.location,
        "workMode": drive.workMode,
        "interviewRounds": drive.interviewRounds,
        "positions": drive.positions,
        "status": drive.status,
        "created_at": drive.created_at.isoformat(),
        "hasApplied": has_applied
    })

# Aplly to sepcific drive
@app.route('/api/student/apply/<int:drive_id>', methods=['POST'])
@jwt_required()
def apply_to_drive(drive_id):

    identity = get_jwt_identity()
    user_id = identity["id"]

    user = User.query.get(user_id)

    if not user or user.type != 'student':
        return {"message": "Unauthorized"}, 403

    drive = Drive.query.get(drive_id)

    if not drive or drive.status != "Active":
        return {"message": "Drive not found or inactive"}, 404

    student = Student.query.filter_by(user_id=user_id).first()

    if not student:
        return {"message": "Student profile not found"}, 404

    # Prevent duplicate applications
    existing_application = Application.query.filter_by(
        student_id=student.id,
        drive_id=drive_id
    ).first()

    if existing_application:
        return {"message": "Already applied to this drive"}, 400

    # Create application
    application = Application(
        student_id=student.id,
        drive_id=drive_id
    )

    db.session.add(application)
    db.session.commit()

    return {"message": "Application submitted successfully"}, 201

# Show all applications of a particular student
@app.route('/api/student/applications', methods=['GET'])
@jwt_required()
def get_student_applications():
    identity = get_jwt_identity()
    user_id = identity["id"]
    user = User.query.get(user_id)
    if not user or user.type != 'student':
        return jsonify({"message": "Unauthorized"}), 403

    cache_key = f"student:apps:{user_id}"
    cached_data = get_cache(cache_key)
    if cached_data:
        print(f"CACHE HIT: {cache_key}")
        return jsonify(cached_data)

    print(f"CACHE MISS: {cache_key}")
    student = Student.query.filter_by(user_id=user_id).first()
    if not student:
        return jsonify([]), 200

    apps = Application.query.filter_by(student_id=student.id).all()

    result = []
    for app_record in apps:
        result.append({
            "id": app_record.id,
            "drive_id": app_record.drive_id,
            "drive_title": app_record.drive.title if app_record.drive else "Unknown",
            "company_name": app_record.drive.company.name if app_record.drive and app_record.drive.company else "Unknown",
            "company_logo": app_record.drive.company.logo if app_record.drive and app_record.drive.company else None,
            "location": app_record.drive.location if app_record.drive else "N/A",
            "workMode": app_record.drive.workMode if app_record.drive else "N/A",
            "payScale": app_record.drive.payScale if app_record.drive else "N/A",
            "status": app_record.status,
            "applied_at": app_record.created_at.isoformat() if app_record.created_at else None,
            "updated_at": app_record.updated_at.isoformat() if app_record.updated_at else None,
            "interviews_scheduled": len(app_record.interviews) if app_record.interviews else 0,
            "comment": app_record.comment
        })

    set_cache(cache_key, result, expiry=60)
    return jsonify(result)


# Get current student profile
@app.route('/api/student/profile', methods=['GET'])
@jwt_required()
def get_student_profile():
    identity = get_jwt_identity()
    user_id = identity["id"]

    user = User.query.get(user_id)
    if not user or user.type != 'student':
        return {"message": "Unauthorized"}, 403

    student = Student.query.filter_by(user_id=user_id).first()
    if not student:
        return jsonify({
            "name": user.name,
            "email": user.email,
            "username": user.username,
            "roll_number": "",
            "branch": "",
            "year_of_study": "",
            "cgpa": "",
            "resume": ""
        }), 200

    return jsonify({
        "id": student.id,
        "name": user.name,
        "email": user.email,
        "username": user.username,
        "roll_number": student.roll_number,
        "branch": student.branch,
        "year_of_study": student.year_of_study,
        "cgpa": student.cgpa,
        "resume": student.resume,
        "blacklisted": user.isBlacklisted
    })


#Upadate Student Profile, if already exists else create new
@app.route('/api/student/profile', methods=['POST'])
@jwt_required()
def create_or_update_student():

    identity = get_jwt_identity()
    user_id = identity["id"]

    user = User.query.get(user_id)

    if not user or user.type != 'student':
        return {"message": "Unauthorized"}, 403

    data = request.get_json()

    # Validate required fields
    required_fields = ["roll_number", "branch", "year_of_study", "cgpa"]
    for field in required_fields:
        if field not in data or data[field] in [None, ""]:
            return {"message": f"{field} is required"}, 400

    student = Student.query.filter_by(user_id=user_id).first()

    # UPDATE existing
    if student:
        student.roll_number = data["roll_number"]
        student.branch = data["branch"]
        student.year_of_study = data["year_of_study"]
        student.cgpa = data["cgpa"]
        student.resume = data.get("resume")

        db.session.commit()

        return {"message": "Student profile updated successfully"}, 200

    # CREATE new
    new_student = Student(
        user_id=user_id,
        roll_number=data["roll_number"],
        branch=data["branch"],
        year_of_study=data["year_of_study"],
        cgpa=data["cgpa"],
        resume=data.get("resume")
    )

    db.session.add(new_student)
    db.session.commit()

    return {"message": "Student profile created successfully"}, 201


@app.route('/api/student/accept-offer/<int:app_id>', methods=['POST'])
@jwt_required()
def accept_offer(app_id):
    identity = get_jwt_identity()
    user_id = identity["id"]
    user = User.query.get(user_id)
    if not user or user.type != 'student':
        return jsonify({"message": "Unauthorized"}), 403

    student = Student.query.filter_by(user_id=user_id).first()
    if not student:
        return jsonify({"message": "Student profile not found"}), 404

    application = Application.query.get(app_id)
    if not application or application.student_id != student.id:
        return jsonify({"message": "Application not found"}), 404

    if application.status.lower() != 'offered':
        return jsonify({"message": "No offer found for this application"}), 400

    application.status = 'placed'
    db.session.commit()

    return jsonify({"message": "Offer accepted successfully. You are now placed!"}), 200