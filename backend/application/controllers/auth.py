from app import app   # import the actual app object
from flask import request, jsonify
from flask_login import login_user, current_user, logout_user
from sqlalchemy import or_
from application.models import User, Company
from app import bcrypt


@app.route("/api/login", methods=["POST"])
def login():

    data = request.get_json()

    identifier = data.get("identifier")
    password = data.get("password")

    if not identifier or not password:
        return jsonify({"error": "Missing credentials"}), 400


    # ---- Check User table ----
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