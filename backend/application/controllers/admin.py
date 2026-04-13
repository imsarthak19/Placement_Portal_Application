from app import app, bcrypt
from flask import request, jsonify
from sqlalchemy import or_
from application.models import User, Company, Drive, Student, Application, Interview
from application.database import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from application.utils import get_cache, set_cache, delete_cache
from application.extensions import redis_client


# API Returns all the company lists for admin dash
@app.route('/api/admin/companies', methods=["GET"])
@jwt_required()
def get_companies():
    user = get_jwt_identity()

    if user["type"] != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    search_query = request.args.get('search', '')

    # Unique cache key per search
    cache_key = f"admin:companies:{search_query}"

    # Check cache first
    cached_data = get_cache(cache_key)
    if cached_data:
        print(f"CACHE HIT: {cache_key}")
        return jsonify(cached_data)
    
    print(f"CACHE MISS: {cache_key}")
    #DB Query only if Cache is Missed
    query = Company.query

    if search_query:
        query = query.filter(
            or_(
                Company.name.ilike(f'%{search_query}%'),
                Company.email.ilike(f'%{search_query}%'),
                Company.industry.ilike(f'%{search_query}%'),
                Company.description.ilike(f'%{search_query}%')
            )
        )

    companies = query.all()
    
    result = [
        {
            "id": c.id,
            "name": c.name,
            "email": c.email,
            "approved": c.approved,
            "icon": c.logo,
            "industry": c.industry,
            "blacklisted": c.isBlacklisted
        } for c in companies
    ]
    
    set_cache(cache_key, result, expiry=60)

    return jsonify(result)


@app.route('/api/admin/all-drives', methods=['GET'])
@jwt_required()
def get_all_drives():
    user = get_jwt_identity()

    if user["type"] != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    search_query = request.args.get('search', '')
    
    query = Drive.query

    if search_query:
        query = query.filter(
            or_(
                Drive.title.ilike(f'%{search_query}%'),
                Drive.description.ilike(f'%{search_query}%'),
                Drive.location.ilike(f'%{search_query}%')
            )
        )

    drives = query.all()

    result = [
        {
            "id": d.id,
            "title": d.title,
            "location": d.location,
            "workMode": d.workMode,
            "status": d.status,
            "payScale": d.payScale,
            "positions": d.positions,
            "company_name": d.company.name,
            "company_logo": d.company.logo,
            "company_id": d.company_id,
            "created_at": d.created_at.isoformat()
        } for d in drives
    ]
    
    return jsonify(result)


# Approve Logic for Company
@app.route('/api/admin/approve_company/<int:company_id>', methods=['PUT'])
@jwt_required()
def approve_company(company_id):
    company = Company.query.get(company_id)

    if not company:
        return {"message": "Company not found"}, 404

    company.approved = True
    db.session.commit()

    return {"message": "Company approved successfully"}


# Blacklist Logic for Company
@app.route('/api/admin/blacklist_company/<int:company_id>', methods=['PUT'])
@jwt_required()
def blacklist_company(company_id):
    company = Company.query.get(company_id)

    if not company:
        return {"message": "Company not found"}, 404

    company.isBlacklisted = True
    db.session.commit()

    return {"message": "Company blacklisted successfully"}


# Whitelist Logic for Company
@app.route('/api/admin/whitelist_company/<int:company_id>', methods=['PUT'])
@jwt_required()
def whitelist_company(company_id):        
    company = Company.query.get(company_id)

    if not company:
        return {"message": "Company not found"}, 404

    company.isBlacklisted = False
    db.session.commit()

    return {"message": "Company whitelisted successfully"}


# Approve Logic for Drive for Admin Dash
@app.route('/api/admin/approve_drive/<int:drive_id>', methods=['PUT'])
@jwt_required()
def approve_drive(drive_id):
    user = get_jwt_identity()
    if user["type"] != "admin":
        return jsonify({"error": "Unauthorized"}), 403
        
    drive = Drive.query.get(drive_id)
    if not drive:
        return jsonify({"message": "Drive not found"}), 404

    drive.status = "Active"
    db.session.commit()
    return jsonify({"message": "Drive approved successfully"})


# Reject Logic for Drive for admin dash
@app.route('/api/admin/reject_drive/<int:drive_id>', methods=['PUT'])
@jwt_required()
def reject_drive(drive_id):
    user = get_jwt_identity()
    if user["type"] != "admin":
        return jsonify({"error": "Unauthorized"}), 403
        
    drive = Drive.query.get(drive_id)
    if not drive:
        return jsonify({"message": "Drive not found"}), 404

    drive.status = "Unapproved"
    db.session.commit()
    return jsonify({"message": "Drive moved back to unapproved successfully"})


# Fetch All Students Logic for Admin
@app.route('/api/admin/all-students', methods=['GET'])
@jwt_required()
def get_all_students():
    user = get_jwt_identity()

    if user["type"] != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    search_query = request.args.get('search', '')
    
    query = User.query.filter_by(type="student")

    if search_query:
        query = query.outerjoin(Student).filter(
            or_(
                User.name.ilike(f'%{search_query}%'),
                User.email.ilike(f'%{search_query}%'),
                Student.branch.ilike(f'%{search_query}%'),
                Student.roll_number.ilike(f'%{search_query}%')
            )
        )

    students = query.all()

    result = [
        {
            "id": s.id,
            "name": s.name,
            "email": s.email,
            "branch": s.student.branch if s.student else 'N/A',
            "blacklisted": s.isBlacklisted,
            "created_at": s.created_at.isoformat()
        } for s in students
    ]
    
    return jsonify(result)


# Blacklist Logic for Student
@app.route('/api/admin/blacklist_student/<int:student_id>', methods=['PUT'])
@jwt_required()
def blacklist_student(student_id):
    student = User.query.get(student_id)

    if not student:
        return {"message": "Student not found"}, 404

    student.isBlacklisted = True
    db.session.commit()

    return {"message": "Student blacklisted successfully"}


# Whitelist Logic for Student
@app.route('/api/admin/whitelist_student/<int:student_id>', methods=['PUT'])
@jwt_required()
def whitelist_student(student_id):
    student = User.query.get(student_id)

    if not student:
        return {"message": "Student not found"}, 404

    student.isBlacklisted = False
    db.session.commit()

    return {"message": "Student whitelisted successfully"}


# Fetch All Applications for Admin Dash
@app.route('/api/admin/all-applications', methods=['GET'])
@jwt_required()
def get_all_applications():
    user = get_jwt_identity()

    if user["type"] != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    search_query = request.args.get('search', '')
    
    # Cache Check
    cache_key = f"admin:applications:{search_query}"
    cached_data = get_cache(cache_key)
    if cached_data:
        print(f"CACHE HIT: {cache_key}")
        return jsonify(cached_data)

    print(f"CACHE MISS: {cache_key}")
    query = Application.query

    if search_query:
        query = query.join(Student).join(User, Student.user_id == User.id).join(Drive).join(Company).filter(
            or_(
                User.name.ilike(f'%{search_query}%'),
                Company.name.ilike(f'%{search_query}%'),
                Drive.title.ilike(f'%{search_query}%'),
                Application.status.ilike(f'%{search_query}%')
            )
        )

    applications = query.all()

    result = [
        {
            "id": a.id,
            "student_id": a.student.user_id if a.student else None,
            "student_name": a.student.user.name if a.student and a.student.user else "Unknown",
            "company_name": a.drive.company.name if a.drive and a.drive.company else "Unknown",
            "drive_title": a.drive.title if a.drive else "Unknown",
            "status": a.status,
            "applied_at": a.created_at.isoformat() if a.created_at else None
        } for a in applications
    ]
    
    set_cache(cache_key, result, expiry=60)

    return jsonify(result)


# Fetch Stats for Admin Dashboard
@app.route('/api/admin/stats', methods=['GET'])
@jwt_required()
def get_admin_stats():
    user = get_jwt_identity()
    if user["type"] != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    # Cache Check
    cache_key = "admin:stats"
    cached_data = get_cache(cache_key)
    if cached_data:
        print(f"CACHE HIT: {cache_key}")
        return jsonify(cached_data)

    print(f"CACHE MISS: {cache_key}")
    students_count = User.query.filter_by(type="student").count()
    companies_count = Company.query.count()
    active_drives_count = Drive.query.filter_by(status='Active').count()
    applications_count = Application.query.count()
    shortlisted_count = Application.query.filter_by(status='shortlisted').count()
    interviews_count = Interview.query.count()

    result = {
        "students": students_count,
        "companies": companies_count,
        "drives": active_drives_count,
        "applications": applications_count,
        "shortlisted": shortlisted_count,
        "interviews": interviews_count
    }
    
    set_cache(cache_key, result, expiry=60)

    return jsonify(result)

@app.route('/api/admin/update-company/<int:company_id>', methods=['PUT', 'POST'])
@jwt_required()
def admin_update_company(company_id):
    user = get_jwt_identity()
    if user["type"] != "admin":
         return jsonify({"error": "Unauthorized"}), 403
    
    company = Company.query.get(company_id)
    if not company:
        return jsonify({"error": "Company not found"}), 404
        
    data = request.get_json()
    
    company.name = data.get('name', company.name)
    company.description = data.get('description', company.description)
    company.industry = data.get('industry', company.industry)
    company.scale = data.get('scale', company.scale)
    company.headOffice = data.get('headOffice', company.headOffice)
    company.website = data.get('website', company.website)
    company.logo = data.get('logo', company.logo)
    company.pocName = data.get('pocName', company.pocName)
    company.pocEmail = data.get('pocEmail', company.pocEmail)
    
    db.session.commit()
    
    return jsonify({"message": "Company profile updated successfully by admin"}), 200

# Get Single Student Profile, will be used by Admin, Company & Student himself
@app.route('/api/admin/student-profile/<int:student_id>', methods=['GET'])
@jwt_required()
def get_student_profile_common(student_id):
    user = get_jwt_identity()
    if user["type"] not in ["admin", "recruiter"]:
        return jsonify({"error": "Unauthorized"}), 403

    cache_key = f"admin:student-profile:{student_id}"
    cached_data = get_cache(cache_key)
    if cached_data:
        print(f"CACHE HIT: {cache_key}")
        return jsonify(cached_data)

    print(f"CACHE MISS: {cache_key}")
    student_user = User.query.get(student_id)
    if not student_user or student_user.type != "student":
        return jsonify({"message": "Student not found"}), 404

    student_details = Student.query.filter_by(user_id=student_user.id).first()

    result = {
        "id": student_user.id,
        "name": student_user.name,
        "email": student_user.email,
        "blacklisted": student_user.isBlacklisted,
        "created_at": student_user.created_at.isoformat() if student_user.created_at else None,
        "roll_number": student_details.roll_number if student_details else None,
        "branch": student_details.branch if student_details else None,
        "year_of_study": student_details.year_of_study if student_details else None,
        "cgpa": student_details.cgpa if student_details else None,
        "resume": student_details.resume if student_details else None
    }
    
    set_cache(cache_key, result, expiry=60)
    return jsonify(result)


# Update Student Profile by Admin/Recruiter
@app.route('/api/admin/update-student/<int:student_id>', methods=['PUT', 'POST'])
@jwt_required()
def admin_update_student_profile(student_id):
    user = get_jwt_identity()
    if user["type"] not in ["admin", "recruiter"]:
         return jsonify({"error": "Unauthorized"}), 403
    
    student_details = Student.query.filter_by(user_id=student_id).first()
    if not student_details:
        return jsonify({"error": "Student profile not found"}), 404
        
    data = request.get_json()
    
    student_details.roll_number = data.get("roll_number", student_details.roll_number)
    student_details.branch = data.get("branch", student_details.branch)
    student_details.year_of_study = data.get("year_of_study", student_details.year_of_study)
    student_details.cgpa = data.get("cgpa", student_details.cgpa)
    student_details.resume = data.get("resume", student_details.resume)
    
    db.session.commit()
    
    # Invalidate cache
    delete_cache(f"admin:student-profile:{student_id}")
    
    return jsonify({"message": "Student profile updated successfully"}), 200

# Get Single Student Applications will be used by Admin and Student himself
@app.route('/api/admin/student-applications/<int:student_id>', methods=['GET'])
@jwt_required()
def get_student_applications_common(student_id):
    user = get_jwt_identity()
    if user["type"] not in ["admin", "recruiter"]:
        return jsonify({"error": "Unauthorized"}), 403

    # For recruiters, caching needs to be specific to their view
    cache_key = f"admin:student-apps:{student_id}:{user['type']}:{user['id'] if user['type'] == 'recruiter' else ''}"
    cached_data = get_cache(cache_key)
    if cached_data:
        print(f"CACHE HIT: {cache_key}")
        return jsonify(cached_data)

    print(f"CACHE MISS: {cache_key}")
    student_details = Student.query.filter_by(user_id=student_id).first()
    if not student_details:
        return jsonify([]), 200

    if user["type"] == "recruiter":
        # Recruiters can ONLY see applications made to THEIR company
        applications = Application.query.join(Drive).filter(
            Application.student_id == student_details.id,
            Drive.company_id == user['id']
        ).all()
    else:
        # Admin can see everything
        applications = Application.query.filter_by(student_id=student_details.id).all()
    
    result = []
    for app_record in applications:
        drive = app_record.drive
        company = drive.company if drive else None
        result.append({
            "id": app_record.id,
            "company_name": company.name if company else "Unknown",
            "drive_title": drive.title if drive else "Unknown",
            "status": app_record.status,
            "applied_at": app_record.created_at.isoformat() if app_record.created_at else None,
            "interviews_scheduled": len(app_record.interviews) if app_record.interviews else 0
        })

    set_cache(cache_key, result, expiry=60)
    return jsonify(result)


# Get Single Drive Details, will be used by Admin, Company & Student himself
@app.route('/api/admin/drive-details/<int:drive_id>', methods=['GET'])
@jwt_required()
def get_drive_details_admin(drive_id):
    user = get_jwt_identity()
    if user["type"] != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    drive = Drive.query.get(drive_id)
    if not drive:
        return jsonify({"message": "Drive found"}), 404

    company = drive.company

    return jsonify({
        "id": drive.id,
        "title": drive.title,
        "description": drive.description,
        "location": drive.location,
        "workMode": drive.workMode,
        "status": drive.status,
        "payScale": drive.payScale,
        "positions": drive.positions,
        "skillsRequired": drive.skillsRequired,
        "educationCriteria": drive.eligibility,
        "batch": drive.batch,
        "company_name": company.name if company else "Unknown",
        "company_id": drive.company_id,
        "company_logo": company.logo if company else None,
        "created_at": drive.created_at.isoformat() if drive.created_at else None
    })


# Get Single Drive Applications, will beused by Admin & Company (for their own drives)
@app.route('/api/admin/drive-applications/<int:drive_id>', methods=['GET'])
@jwt_required()
def get_drive_applications(drive_id):
    user = get_jwt_identity()
    if user["type"] != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    cache_key = f"admin:drive-apps:{drive_id}"
    cached_data = get_cache(cache_key)
    if cached_data:
        print(f"CACHE HIT: {cache_key}")
        return jsonify(cached_data)

    print(f"CACHE MISS: {cache_key}")
    applications = Application.query.filter_by(drive_id=drive_id).all()
    
    result = []
    for app_record in applications:
        student_model = app_record.student
        user_model = student_model.user if student_model else None
        
        result.append({
            "id": app_record.id,
            "student_id": user_model.id if user_model else None,
            "student_name": user_model.name if user_model else "Unknown",
            "roll_number": student_model.roll_number if student_model else "N/A",
            "branch": student_model.branch if student_model else "N/A",
            "cgpa": student_model.cgpa if student_model else "N/A",
            "status": app_record.status,
            "applied_at": app_record.created_at.isoformat() if app_record.created_at else None
        })

    set_cache(cache_key, result, expiry=60)
    return jsonify(result)