from app import app, bcrypt
from flask import request, jsonify
from sqlalchemy import or_
from application.models import User, Company
from application.database import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

# LOGIN
@app.route("/api/login", methods=["POST"])
def login():

    data = request.get_json()

    identifier = data.get("identifier")
    password = data.get("password")

    if not identifier or not password:
        return jsonify({"error": "Missing credentials"}), 400
    


    account = User.query.filter(
        or_(
            User.email == identifier,
            User.username == identifier
        )
    ).first()

    if account and account.type == "student" and account.isBlacklisted:
        return jsonify({
            "error": "Student account is blacklisted. Contact support."
        }), 403

    account_type = None

    if account:
        account_type = account.type

    # Check Company
    if not account:
        account = Company.query.filter(
            or_(
                Company.email == identifier,
                Company.username == identifier
            )
        ).first()

        if account:
            account_type = "recruiter"

            if not account.approved:
                return jsonify({
                    "error": "Recruiter account not approved by admin."
                }), 403
            
            elif account and account.isBlacklisted:
                return jsonify({
                    "error": "Recruiter account is blacklisted. Contact support."
                }), 403

    if not account:
        return jsonify({"error": "User not found"}), 404

    if not bcrypt.check_password_hash(account.password, password):
        return jsonify({"error": "Invalid password"}), 401

    # JWT Implemented here
    token = create_access_token(identity={
        "id": account.id,
        "type": account_type,
        "username": account.username
    })

    return jsonify({
        "message": "Login successful",
        "token": token,
        "type": account_type,
        "username": account.username
    })


# GET CURRENT USER 
@app.route("/api/me", methods=["GET"])
@jwt_required()
def get_current_user():

    user = get_jwt_identity()

    return jsonify({
        "authenticated": True,
        "user_id": user["id"],
        "username": user["username"],
        "type": user["type"]
    })


# STUDENT REGISTER 
@app.route("/api/student-register", methods=["POST"])
def student_register():

    data = request.get_json()

    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    if not name or not email or not username or not password:
        return jsonify({"error": "All fields are required."}), 400

    if len(username) < 4:
        return jsonify({"error": "Username must be at least 4 characters."}), 400

    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters."}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists."}), 409

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already taken."}), 409

    hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")

    user = User(
        name=name,
        email=email,
        username=username,
        password=hashed_pw,
        type="student"
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "Student account created successfully."
    }), 201


# COMPANY REGISTER
@app.route("/api/company-register", methods=["POST"])
def company_register():

    data = request.get_json()

    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    if not name or not email or not username or not password:
        return jsonify({"error": "All fields are required."}), 400

    if len(username) < 4:
        return jsonify({"error": "Username must be at least 4 characters."}), 400

    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters."}), 400

    if Company.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists."}), 409

    if Company.query.filter_by(username=username).first():
        return jsonify({"error": "Username already taken."}), 409

    hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")

    company = Company(
        name=name,
        email=email,
        username=username,
        password=hashed_pw,
        approved=False
    )

    db.session.add(company)
    db.session.commit()

    return jsonify({
        "message": "Company account created. Await admin approval."
    }), 201