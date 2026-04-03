from app import app   # import the actual app object
from flask import request, jsonify
from flask_login import login_user, current_user, logout_user
from sqlalchemy import or_
from application.models import User, Company
from application.database import db
from app import bcrypt

# Login API
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
    
    account_type = None

    if account:
        account_type = account.type

    # ---- If not found, check Company table ----
    if not account:
        account = Company.query.filter(
            or_(
                Company.email == identifier,
                Company.username == identifier
            )
        ).first()

        if account:
            account_type = "recruiter"


    if not account:
        return jsonify({"error": "User not found"}), 404


    if not bcrypt.check_password_hash(account.password, password):
        return jsonify({"error": "Invalid password"}), 401


    login_user(account)


    return jsonify({
        "message": "Login successful",
        "user_id": account.id,
        "type": account_type
    })



# Logout API
@app.route("/api/logout", methods=["POST"])
def logout():

    logout_user()

    return jsonify({
        "message": "Logout successful"
    })



#Will be using this function in the future to detect account type in a more elegant way, currently we are doing it in a bit of a hacky way by checking the instance type in multiple places, this will help us centralize that logic in one place and make it more maintainable in the long run.
def get_account_type(user):
    if isinstance(user, Company):
        return "recruiter"
    return user.type



# Returns user info API
@app.route("/api/me", methods=["GET"])
def get_current_user():

    if not current_user.is_authenticated:
        return jsonify({
            "authenticated": False
        })

    # detect account type
    if isinstance(current_user, Company):
        account_type = "recruiter"
    else:
        account_type = current_user.type

    return jsonify({
        "authenticated": True,
        "user_id": current_user.id,
        "username": current_user.username,
        "type": account_type
    })



# Student Register or Signup
@app.route("/api/student-register", methods=["POST"])
def student_register():
    data = request.get_json()

    name     = (data.get("name") or "").strip()
    email    = (data.get("email") or "").strip()
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    # ---- Basic validation ----
    if not name or not email or not username or not password:
        return jsonify({"error": "All fields are required."}), 400

    if len(username) < 4:
        return jsonify({"error": "Username must be at least 4 characters."}), 400

    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters."}), 400

    # ---- Uniqueness checks ----
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "An account with this email already exists."}), 409

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "This username is already taken."}), 409

    # ---- Create student user ----
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

    login_user(user)

    return jsonify({
        "message": "Student account created successfully.",
        "user_id": user.id
    }), 201



# Company Register or Signup
@app.route("/api/company-register", methods=["POST"])
def company_register():
    data = request.get_json()

    name     = (data.get("name") or "").strip()
    email    = (data.get("email") or "").strip()
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    # ---- Basic validation ----
    if not name or not email or not username or not password:
        return jsonify({"error": "All fields are required."}), 400

    if len(username) < 4:
        return jsonify({"error": "Username must be at least 4 characters."}), 400

    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters."}), 400

    # ---- Uniqueness checks ----
    if Company.query.filter_by(email=email).first():
        return jsonify({"error": "An account with this email already exists."}), 409

    if Company.query.filter_by(username=username).first():
        return jsonify({"error": "This username is already taken."}), 409

    # ---- Create company ----
    hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")
    company = Company(
        name=name,
        email=email,
        username=username,
        password=hashed_pw,
    )
    db.session.add(company)
    db.session.commit()

    login_user(company)

    return jsonify({
        "message": "Company account created successfully.",
        "company_id": company.id
    }), 201