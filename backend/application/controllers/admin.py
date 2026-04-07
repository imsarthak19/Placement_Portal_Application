from app import app, bcrypt
from flask import request, jsonify
from sqlalchemy import or_
from application.models import User, Company, Drive
from application.database import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from flask_jwt_extended import jwt_required, get_jwt_identity

@app.route('/api/admin/companies', methods=["GET"])
@jwt_required()
def get_companies():

    user = get_jwt_identity()

    if user["type"] != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    companies = Company.query.all()

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

# Fetch All Drives for a Company
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
            "created_at": d.created_at.isoformat()
        } for d in drives
    ])

#Fetch All Drives by all companies
@app.route('/api/admin/all-drives', methods=['GET'])
@jwt_required()
def get_all_drives():
    user = get_jwt_identity()

    if user["type"] != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    drives = Drive.query.all()

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
            "company_id": d.company_id,
            "created_at": d.created_at.isoformat()
        } for d in drives
    ])

# Approve Logic for Drive
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

# Reject Logic for Drive
@app.route('/api/admin/reject_drive/<int:drive_id>', methods=['PUT'])
@jwt_required()
def reject_drive(drive_id):
    user = get_jwt_identity()
    if user["type"] != "admin":
        return jsonify({"error": "Unauthorized"}), 403
        
    drive = Drive.query.get(drive_id)
    if not drive:
        return jsonify({"message": "Drive not found"}), 404

    drive.status = "Rejected"
    db.session.commit()
    return jsonify({"message": "Drive rejected successfully"})


# Fetch All Students Logic for Admin
@app.route('/api/admin/all-students', methods=['GET'])
@jwt_required()
def get_all_students():
    user = get_jwt_identity()

    if user["type"] != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    students = User.query.filter_by(type="student").all()

    return jsonify([
        {
            "id": s.id,
            "name": s.name,
            "email": s.email,
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