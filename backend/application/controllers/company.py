from app import app, bcrypt
from flask import request, jsonify
from sqlalchemy import or_
from application.models import User, Company, Drive, Application
from application.database import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import datetime

# Create Drive
@app.route('/api/company/create-drive', methods=['POST'])
@jwt_required()
def create_drive():
    user = get_jwt_identity()
    if user["type"] != "recruiter":
         return jsonify({"error": "Unauthorized"}), 403
    
    data = request.get_json()
    
    title = data.get('title')
    if not title:
        return jsonify({"error": "Title is required"}), 400
        
    new_drive = Drive(
        company_id=user['id'],
        title=title,
        description=data.get('description'),
        eligibility=data.get('eligibility'),
        batch=data.get('batch'),
        branches=data.get('branches'),
        skillsRequired=data.get('skillsRequired'),
        payScale=data.get('payScale'),
        location=data.get('location'),
        workMode=data.get('workMode'),
        interviewRounds=data.get('interviewRounds'),
        positions=data.get('positions'),
        status='Unapproved'
    )
    
    deadline_str = data.get('deadline')
    if deadline_str:
        try:
            # Handle ISO format from frontend
            new_drive.deadline = datetime.datetime.fromisoformat(deadline_str.replace('Z', '+00:00'))
        except ValueError:
            pass
            
    db.session.add(new_drive)
    db.session.commit()
    
    return jsonify({"message": "Drive created successfully", "id": new_drive.id}), 201

# Update Drive
@app.route('/api/company/update-drive/<int:drive_id>', methods=['PUT', 'POST'])
@jwt_required()
def update_drive(drive_id):
    user = get_jwt_identity()
    if user["type"] != "recruiter":
         return jsonify({"error": "Unauthorized"}), 403
    
    drive = Drive.query.get(drive_id)
    if not drive or drive.company_id != user['id']:
        return jsonify({"error": "Drive not found or unauthorized"}), 404
        
    data = request.get_json()
    
    drive.title = data.get('title', drive.title)
    drive.description = data.get('description', drive.description)
    drive.eligibility = data.get('eligibility', drive.eligibility)
    drive.batch = data.get('batch', drive.batch)
    drive.branches = data.get('branches', drive.branches)
    drive.skillsRequired = data.get('skillsRequired', drive.skillsRequired)
    drive.payScale = data.get('payScale', drive.payScale)
    drive.location = data.get('location', drive.location)
    drive.workMode = data.get('workMode', drive.workMode)
    drive.interviewRounds = data.get('interviewRounds', drive.interviewRounds)
    drive.positions = data.get('positions', drive.positions)
    
    deadline_str = data.get('deadline')
    if deadline_str:
        try:
            drive.deadline = datetime.datetime.fromisoformat(deadline_str.replace('Z', '+00:00'))
        except ValueError:
            pass
            
    db.session.commit()
    
    return jsonify({"message": "Drive updated successfully"}), 200

# Close Drive manually
@app.route('/api/company/close-drive/<int:drive_id>', methods=['PUT'])
@jwt_required()
def close_drive(drive_id):
    user = get_jwt_identity()
    if user["type"] != "recruiter":
         return jsonify({"error": "Unauthorized"}), 403
    
    drive = Drive.query.get(drive_id)
    if not drive or drive.company_id != user['id']:
        return jsonify({"error": "Drive not found or unauthorized"}), 404
        
    drive.status = 'Closed'
    db.session.commit()
    
    return jsonify({"message": "Drive closed successfully"}), 200

# Get Drive Details
@app.route('/api/company/drive-details/<int:drive_id>', methods=['GET'])
@jwt_required()
def get_company_drive_details(drive_id):
    user = get_jwt_identity()
    if user["type"] != "recruiter":
         return jsonify({"error": "Unauthorized"}), 403
    
    drive = Drive.query.get(drive_id)
    if not drive or drive.company_id != user['id']:
        return jsonify({"error": "Drive not found or unauthorized"}), 404
        
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
        "eligibility": drive.eligibility,
        "batch": drive.batch,
        "branches": drive.branches,
        "deadline": drive.deadline.isoformat() if drive.deadline else None,
        "interviewRounds": drive.interviewRounds,
        "created_at": drive.created_at.isoformat() if drive.created_at else None,
        "company_name": drive.company.name,
        "company_logo": drive.company.logo
    })

# Get Applications for a Drive
@app.route('/api/company/drive-applications/<int:drive_id>', methods=['GET'])
@jwt_required()
def get_company_drive_applications(drive_id):
    user = get_jwt_identity()
    if user["type"] != "recruiter":
        return jsonify({"error": "Unauthorized"}), 403

    drive = Drive.query.get(drive_id)
    if not drive or drive.company_id != user['id']:
        return jsonify({"error": "Drive not found or unauthorized"}), 404

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

# Get All Applications for Company
@app.route('/api/company/all-applications', methods=['GET'])
@jwt_required()
def get_company_all_applications():
    user = get_jwt_identity()
    if user["type"] != "recruiter":
        return jsonify({"error": "Unauthorized"}), 403

    # Fetch all applications for all drives belonging to this company
    applications = Application.query.join(Drive).filter(Drive.company_id == user['id']).all()
    
    apps_data = []
    for app_record in applications:
        student_model = app_record.student
        user_model = student_model.user if student_model else None
        
        apps_data.append({
            "id": app_record.id,
            "student_id": user_model.id if user_model else None,
            "student_name": user_model.name if user_model else "Unknown",
            "drive_title": app_record.drive.title,
            "drive_id": app_record.drive_id,
            "roll_number": student_model.roll_number if student_model else "N/A",
            "branch": student_model.branch if student_model else "N/A",
            "cgpa": student_model.cgpa if student_model else "N/A",
            "status": app_record.status,
            "applied_at": app_record.created_at.isoformat() if app_record.created_at else None
        })

    return jsonify(apps_data)

# Update Application Status
@app.route('/api/company/update-application-status/<int:app_id>', methods=['PUT', 'POST'])
@jwt_required()
def update_application_status(app_id):
    user = get_jwt_identity()
    if user["type"] != "recruiter":
        return jsonify({"error": "Unauthorized"}), 403

    application = Application.query.get(app_id)
    if not application:
        return jsonify({"error": "Application not found"}), 404

    # Ensure the drive belongs to the recruiter's company
    if application.drive.company_id != user['id']:
        return jsonify({"error": "Unauthorized to update this application"}), 403

    data = request.get_json()
    new_status = data.get('status')
    comment = data.get('comment')

    if not new_status:
        return jsonify({"error": "Status is required"}), 400

    valid_statuses = ['applied', 'shortlisted', 'interviewing', 'rejected', 'selected', 'offered', 'hired']
    if new_status.lower() not in valid_statuses:
        return jsonify({"error": "Invalid status"}), 400

    application.status = new_status.lower()
    if comment is not None:
        application.comment = comment

    db.session.commit()

    return jsonify({"message": f"Application status updated to {new_status}"}), 200

# Update Company Profile
@app.route('/api/company/update-profile', methods=['PUT', 'POST'])
@jwt_required()
def update_company_profile():
    user = get_jwt_identity()
    if user["type"] != "recruiter":
         return jsonify({"error": "Unauthorized"}), 403
    
    company = Company.query.get(user['id'])
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
    
    return jsonify({"message": "Profile updated successfully"}), 200

# Get Shortlisted Applications for Company
@app.route('/api/company/shortlisted-applications', methods=['GET'])
@jwt_required()
def get_shortlisted_applications():
    user = get_jwt_identity()
    if user["type"] != "recruiter":
        return jsonify({"error": "Unauthorized"}), 403

    # Get all drives for this company
    drives = Drive.query.filter_by(company_id=user['id']).all()
    drive_ids = [d.id for d in drives]

    # Get all shortlisted applications for these drives
    shortlisted_apps = Application.query.filter(
        Application.drive_id.in_(drive_ids),
        Application.status == 'shortlisted'
    ).order_by(Application.created_at.desc()).all()

    output = []
    for app_record in shortlisted_apps:
        student_model = app_record.student
        user_model = student_model.user
        drive_model = app_record.drive
        
        output.append({
            "id": app_record.id,
            "student_id": user_model.id,
            "student_name": user_model.name,
            "roll_number": student_model.roll_number,
            "branch": student_model.branch,
            "cgpa": student_model.cgpa,
            "drive_title": drive_model.title,
            "status": app_record.status,
            "applied_at": app_record.created_at.isoformat(),
            "interviews": [{
                "id": i.id,
                "scheduled_at": i.scheduled_at.isoformat(),
                "mode": i.mode,
                "meeting_link": i.meeting_link,
                "location": i.location
            } for i in app_record.interviews]
        })

    return jsonify(output), 200

# Schedule Interview for an Application
@app.route('/api/company/schedule-interview/<int:app_id>', methods=['POST'])
@jwt_required()
def schedule_interview(app_id):
    user = get_jwt_identity()
    if user["type"] != "recruiter":
        return jsonify({"error": "Unauthorized"}), 403

    application = Application.query.get(app_id)
    if not application:
        return jsonify({"error": "Application not found"}), 404

    if application.drive.company_id != user['id']:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    scheduled_at_str = data.get('scheduled_at')
    mode = data.get('mode')
    location = data.get('location')
    meeting_link = data.get('meeting_link')

    if not scheduled_at_str or not mode:
        return jsonify({"error": "Date and mode are required"}), 400

    try:
        from application.models import Interview
        # Parse ISO datetime
        scheduled_at = datetime.datetime.fromisoformat(scheduled_at_str.replace('Z', '+00:00'))
        
        new_interview = Interview(
            application_id=app_id,
            scheduled_at=scheduled_at,
            mode=mode,
            location=location,
            meeting_link=meeting_link
        )

        # Automatically update application status if it was just 'shortlisted'
        if application.status == 'shortlisted':
            application.status = 'interviewing'

        db.session.add(new_interview)
        db.session.commit()

        return jsonify({"message": "Interview scheduled successfully", "id": new_interview.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Get All Interviews for Company
@app.route('/api/company/interviews', methods=['GET'])
@jwt_required()
def get_company_interviews():
    user = get_jwt_identity()
    if user["type"] != "recruiter":
        return jsonify({"error": "Unauthorized"}), 403

    # Get all drives for this company
    drives = Drive.query.filter_by(company_id=user['id']).all()
    drive_ids = [d.id for d in drives]

    # Get all applications for these drives
    apps = Application.query.filter(Application.drive_id.in_(drive_ids)).all()
    app_ids = [app.id for app in apps]

    # Get all interviews for these application IDs
    from application.models import Interview
    interviews = Interview.query.filter(Interview.application_id.in_(app_ids)).order_by(Interview.scheduled_at.desc()).all()

    output = []
    for i in interviews:
        app_record = i.application
        student_model = app_record.student
        user_model = student_model.user
        drive_model = app_record.drive

        output.append({
            "id": i.id,
            "application_id": app_record.id,
            "student_name": user_model.name,
            "student_id": user_model.id,
            "drive_title": drive_model.title,
            "scheduled_at": i.scheduled_at.isoformat(),
            "mode": i.mode,
            "location": i.location,
            "meeting_link": i.meeting_link,
            "created_at": i.created_at.isoformat()
        })

    return jsonify(output), 200


# Get Company Stats
@app.route('/api/company/stats', methods=['GET'])
@jwt_required()
def get_company_stats():
    user = get_jwt_identity()
    if user["type"] != "recruiter":
        return jsonify({"error": "Unauthorized"}), 403

    company_id = user['id']
    from application.models import Drive, Application, Interview
    
    total_drives = Drive.query.filter_by(company_id=company_id).count()
    active_drives = Drive.query.filter_by(company_id=company_id, status='Active').count()
    
    apps_query = Application.query.join(Drive).filter(Drive.company_id == company_id)
    total_applications = apps_query.count()
    shortlisted_applications = apps_query.filter(Application.status == 'shortlisted').count()
    hired_candidates = apps_query.filter(Application.status == 'hired').count()
    
    interviews_count = Interview.query.join(Application).join(Drive).filter(Drive.company_id == company_id).count()

    return jsonify({
        "total_drives": total_drives,
        "active_drives": active_drives,
        "total_applications": total_applications,
        "shortlisted": shortlisted_applications,
        "hired": hired_candidates,
        "interviews": interviews_count
    })