from app import app, bcrypt
from flask import request, jsonify
from sqlalchemy import or_
from application.models import User, Company, Drive, Student, Application, Interview
from application.database import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


# API Returns all the company lists for admin dash
@app.route('/api/admin/companies', methods=["GET"])
@jwt_required()
def get_companies():
    user = get_jwt_identity()

    if user["type"] != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    search_query = request.args.get('search', '')
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

    return jsonify([
        {
            "id": c.id,
            "name": c.name,
            "email": c.email,
            "approved": c.approved,
            "icon": c.logo,
            "industry": c.industry,
            "blacklisted": c.isBlacklisted
        } for c in companies
    ])


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

    return jsonify([
        {
            "id": s.id,
            "name": s.name,
            "email": s.email,
            "branch": s.student.branch if s.student else 'N/A',
            "blacklisted": s.isBlacklisted,
            "created_at": s.created_at.isoformat()
        } for s in students
    ])


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

    return jsonify([
        {
            "id": a.id,
            "student_name": a.student.user.name if a.student and a.student.user else "Unknown",
            "company_name": a.drive.company.name if a.drive and a.drive.company else "Unknown",
            "drive_title": a.drive.title if a.drive else "Unknown",
            "status": a.status,
            "applied_at": a.created_at.isoformat() if a.created_at else None
        } for a in applications
    ])


# Fetch Stats for Admin Dashboard
@app.route('/api/admin/stats', methods=['GET'])
@jwt_required()
def get_admin_stats():
    user = get_jwt_identity()
    if user["type"] != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    students_count = User.query.filter_by(type="student").count()
    companies_count = Company.query.count()
    active_drives_count = Drive.query.filter_by(status='Active').count()
    applications_count = Application.query.count()
    shortlisted_count = Application.query.filter_by(status='shortlisted').count()
    interviews_count = Interview.query.count()

    return jsonify({
        "students": students_count,
        "companies": companies_count,
        "drives": active_drives_count,
        "applications": applications_count,
        "shortlisted": shortlisted_count,
        "interviews": interviews_count
    })

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