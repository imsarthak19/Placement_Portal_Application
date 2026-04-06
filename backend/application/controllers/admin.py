from app import app, bcrypt
from flask import request, jsonify
from sqlalchemy import or_
from application.models import User, Company
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