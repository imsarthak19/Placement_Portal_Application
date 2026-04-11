from flask import request, jsonify
from application.models import User, Student, Company, Drive, Application
from application.database import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import app
from sqlalchemy import or_


@app.route('/api/student/active-drives', methods=['GET'])
@jwt_required()
def get_active_drives():

    identity = get_jwt_identity()
    user_id = identity["id"]

    user = User.query.get(user_id)

    if not user or user.type != 'student':
        return {"message": "Unauthorized"}, 403

    search = request.args.get('search', '')

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

    if not drives:
        return {"message": "No active drives found"}, 404

    return jsonify([
        {
            "id": d.id,
            "title": d.title,
            "company_name": d.company.name,
            "company_logo": d.company.logo,
            "location": d.location,
            "workMode": d.workMode,
            "status": d.status,
            "payScale": d.payScale,
            "positions": d.positions,
            "created_at": d.created_at.isoformat()
        } for d in drives
    ])


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

    if not drive or drive.status != "Active":
        return {"message": "Drive not found or inactive"}, 404

    return jsonify({
        "id": drive.id,
        "title": drive.title,
        "company_name": drive.company.name,
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
        "created_at": drive.created_at.isoformat()
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

    student = Student.query.filter_by(user_id=user_id).first()
    if not student:
        return jsonify([]), 200

    apps = Application.query.filter_by(student_id=student.id).all()

    output = []
    for app in apps:
        output.append({
            "id": app.id,
            "drive_id": app.drive_id,
            "drive_title": app.drive.title,
            "company_name": app.drive.company.name,
            "status": app.status,
            "applied_at": app.created_at.isoformat(),
            "updated_at": app.updated_at.isoformat(),
            "interviews_scheduled": len(app.interviews)
        })

    return jsonify(output), 200


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