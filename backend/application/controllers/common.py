from app import app, bcrypt
from flask import request, jsonify
from sqlalchemy import or_
from application.models import User, Company, Drive, Student, Application
from application.database import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


# API Returns the company profile for the company, will use it in Admin, Company and Student Dashboard
@app.route('/api/company-profile/<int:company_id>', methods=['GET'])
@jwt_required()
def get_company_profile(company_id):
    company = Company.query.get(company_id)

    if not company:
        return {"message": "Company not found"}, 404

    return jsonify({
        "name": company.name,
        "email": company.email,
        "approved": company.approved,
        'description': company.description,
        "scale": company.scale,
        "headOffice": company.headOffice,
        "website": company.website,
        'pocName': company.pocName,
        'pocEmail': company.pocEmail,
        "icon": company.logo,
        "industry": company.industry,
        "blacklisted": company.isBlacklisted,
        "created_at": company.created_at.isoformat()
    })


# Fetch All Drives of a particular Company
@app.route('/api/company/all-drives/<int:company_id>', methods=['GET'])
@jwt_required()
def get_company_drives(company_id):
    company = Company.query.get(company_id)

    if not company:
        return {"message": "Company not found"}, 404
    
    if not company.drives:
        return {"message": "No drives found for this company"}, 404

    drives = company.drives

    return jsonify([
        {
            "id": d.id,
            "title": d.title,
            "location": d.location,
            "workMode": d.workMode,
            "status": d.status,
            "payScale": d.payScale,
            "positions": d.positions,
            "company_name": company.name,
            "company_logo": company.logo,
            "created_at": d.created_at.isoformat()
        } for d in drives
    ])


#Fetch All Drives by all companies, will be used by Admin & Students
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

    return jsonify([
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
    ])


# Get Single Student Profile, will be used by Admin, Company & Student himself
@app.route('/api/admin/student-profile/<int:student_id>', methods=['GET'])
@jwt_required()
def get_student_profile_common(student_id):
    user = get_jwt_identity()
    if user["type"] not in ["admin", "recruiter"]:
        return jsonify({"error": "Unauthorized"}), 403

    student_user = User.query.get(student_id)
    if not student_user or student_user.type != "student":
        return jsonify({"message": "Student not found"}), 404

    student_details = Student.query.filter_by(user_id=student_user.id).first()

    return jsonify({
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
    })


# Get Single Student Applications will be used by Admin and Student himself
@app.route('/api/admin/student-applications/<int:student_id>', methods=['GET'])
@jwt_required()
def get_student_applications_common(student_id):
    user = get_jwt_identity()
    if user["type"] not in ["admin", "recruiter"]:
        return jsonify({"error": "Unauthorized"}), 403

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
    
    apps_data = []
    for app_record in applications:
        drive = app_record.drive
        company = drive.company if drive else None
        apps_data.append({
            "id": app_record.id,
            "company_name": company.name if company else "Unknown",
            "drive_title": drive.title if drive else "Unknown",
            "status": app_record.status,
            "applied_at": app_record.created_at.isoformat() if app_record.created_at else None,
            "interviews_scheduled": len(app_record.interviews) if app_record.interviews else 0
        })

    return jsonify(apps_data)


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

    applications = Application.query.filter_by(drive_id=drive_id).all()
    
    apps_data = []
    for app_record in applications:
        student_model = app_record.student
        user_model = student_model.user if student_model else None
        
        apps_data.append({
            "id": app_record.id,
            "student_id": user_model.id if user_model else None,
            "student_name": user_model.name if user_model else "Unknown",
            "roll_number": student_model.roll_number if student_model else "N/A",
            "branch": student_model.branch if student_model else "N/A",
            "cgpa": student_model.cgpa if student_model else "N/A",
            "status": app_record.status,
            "applied_at": app_record.created_at.isoformat() if app_record.created_at else None
        })

    return jsonify(apps_data)
