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
            "approved": c.approved
        } for c in companies
    ])