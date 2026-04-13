from celery_worker import celery
import time
import csv
import io
import datetime
from application.models import Drive, Application, Company, User, Student
from application.database import db

# Simulate email sending
@celery.task(bind=True)
def send_interview_email(self, student_email, drive_title):
    print(f"Sending email to {student_email} for {drive_title}")
    
    time.sleep(5)  # simulate delay

    print(f"Email sent to {student_email}")

    return {
        "status": "sent",
        "email": student_email
    }


# Reminder task
@celery.task(bind=True)
def send_reminder_email(self, student_email):
    print(f"Sending reminder to {student_email}")

    time.sleep(3)

    print(f"Reminder sent to {student_email}")

    return {
        "status": "reminder_sent",
        "email": student_email
    }


# Export Company CSV task
@celery.task(bind=True)
def export_company_data_csv(self, company_id, recruiter_email):
    print(f"Starting CSV export for company {company_id}")
    
    time.sleep(2) 
    
    from app import app
    with app.app_context():
        applications = Application.query.join(Drive).filter(Drive.company_id == company_id).all()
        
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Application ID', 'Student Name', 'Roll Number', 'Drive Title', 'Status', 'Date Applied'])
        
        for app_record in applications:
            writer.writerow([
                app_record.id,
                app_record.student.user.name,
                app_record.student.roll_number,
                app_record.drive.title,
                app_record.status,
                app_record.created_at.strftime('%Y-%m-%d %H:%M') if app_record.created_at else 'N/A'
            ])
            
        csv_content = output.getvalue()
        output.close()
        
        # Simulate sending email with attachment
        print(f"Emailing CSV report to {recruiter_email}...")
        time.sleep(3)
        print(f"CSV Export task complete for {recruiter_email}")

    return {"status": "success", "recruiter_email": recruiter_email}


# Student CSV Export task
@celery.task(bind=True)
def export_student_data_csv(self, student_id, student_email):
    print(f"Starting Student CSV export for ID: {student_id}")
    time.sleep(2)
    
    from app import app
    with app.app_context():
        applications = Application.query.filter_by(student_id=student_id).all()
        
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Application ID', 'Company Name', 'Drive Title', 'Pay Scale', 'Current Status', 'Applied Date'])
        
        for app_record in applications:
            writer.writerow([
                app_record.id,
                app_record.drive.company.name,
                app_record.drive.title,
                app_record.drive.payScale,
                app_record.status,
                app_record.created_at.strftime('%Y-%m-%d %H:%M') if app_record.created_at else 'N/A'
            ])
            
        csv_content = output.getvalue()
        output.close()
        
        print(f"Emailing CSV history to {student_email}...")
        time.sleep(2)
        print(f"Student Export task complete!")

    return {"status": "success", "email": student_email}


# Monthly Placement Report (Batch Job - HTML)
@celery.task(bind=True)
def generate_monthly_placement_reports(self):
    print("Running Monthly Batched Placement Reports...")
    from app import app
    with app.app_context():
        # Get all approved companies
        companies = Company.query.filter_by(approved=True).all()
        
        for company in companies:
            # Find all placements for this company in the last 30 days
            last_month = datetime.datetime.now() - datetime.timedelta(days=30)
            placements = Application.query.join(Drive).filter(
                Drive.company_id == company.id,
                Application.status.in_(['placed', 'hired']),
                Application.updated_at >= last_month
            ).all()
            
            # Generate HTML Report
            html_report = f"""
            <html>
                <body style="font-family: sans-serif; color: #333;">
                    <h1 style="color: #781f19;">Monthly Placement Report - {company.name}</h1>
                    <p>Reporting Period: {last_month.strftime('%B %Y')} to Present</p>
                    <hr/>
                    <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                        <h2>Summary Metrics</h2>
                        <ul>
                            <li><strong>New Placements:</strong> {len(placements)}</li>
                            <li><strong>Report ID:</strong> RPT-{company.id}-{datetime.datetime.now().strftime('%m%Y')}</li>
                        </ul>
                    </div>
                    
                    <h3>Placement Breakdown</h3>
                    <table border="1" cellpadding="10" style="border-collapse: collapse; width: 100%;">
                        <tr style="background: #f2f2f2;">
                            <th>Student</th>
                            <th>Drive Title</th>
                            <th>Package</th>
                            <th>Date</th>
                        </tr>
            """
            
            for p in placements:
                html_report += f"""
                        <tr>
                            <td>{p.student.user.name}</td>
                            <td>{p.drive.title}</td>
                            <td>{p.drive.payScale}</td>
                            <td>{p.updated_at.strftime('%Y-%m-%d')}</td>
                        </tr>
                """
            
            if not placements:
                html_report += "<tr><td colspan='4' align='center'>No placements recorded in this period.</td></tr>"
                
            html_report += """
                    </table>
                    <p style="margin-top: 30px; font-size: 0.8em; color: #666;">
                        Generated automatically by CampusBridge Placement System.
                    </p>
                </body>
            </html>
            """
            
            print(f"Sending Monthly HTML Report to {company.email}...")
            
    print("All monthly reports generated and dispatched.")
    return {"status": "batch_complete"}


# Daily Interview Reminders (Beat Job)
@celery.task(bind=True)
def send_daily_interview_reminders(self):
    print("Running Scheduled Interview Reminders...")
    from app import app
    with app.app_context():
        # Find interviews happening in the next 24 hours
        tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
        now = datetime.datetime.now()
        
        upcoming_interviews = Interview.query.filter(
            Interview.scheduled_at >= now,
            Interview.scheduled_at <= tomorrow
        ).all()
        
        for interview in upcoming_interviews:
            student_email = interview.application.student.user.email
            print(f"Automatic Reminder: Queuing email for {student_email}")
            # We can directly call the function or trigger another task
            send_reminder_email.delay(student_email)
            
    return {"status": "reminders_queued", "count": len(upcoming_interviews)}


# Platform Wide Report for Admin
@celery.task(bind=True)
def generate_platform_report_csv(self, admin_email):
    print(f"Starting Platform Wide CSV export for admin: {admin_email}")
    time.sleep(5)  # simulate intensive work
    
    from app import app
    with app.app_context():
        # Get overall stats for the report
        total_students = Student.query.count()
        total_companies = Company.query.count()
        total_applications = Application.query.count()
        total_placed = Application.query.filter(Application.status.in_(['placed', 'hired'])).count()
        
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Platform Placement Report', 'Date:', datetime.datetime.now().strftime('%Y-%m-%d')])
        writer.writerow([])
        writer.writerow(['Metric', 'Value'])
        writer.writerow(['Total Students', total_students])
        writer.writerow(['Total Companies', total_companies])
        writer.writerow(['Total Applications', total_applications])
        writer.writerow(['Total Placements', total_placed])
        writer.writerow([])
        writer.writerow(['Recent Placements'])
        writer.writerow(['Student', 'Company', 'Drive', 'Package', 'Status', 'Date'])
        
        recent_placements = Application.query.filter(Application.status.in_(['placed', 'hired'])).limit(100).all()
        for p in recent_placements:
             writer.writerow([
                p.student.user.name if p.student and p.student.user else "N/A",
                p.drive.company.name if p.drive and p.drive.company else "N/A",
                p.drive.title if p.drive else "N/A",
                p.drive.payScale if p.drive else "N/A",
                p.status,
                p.updated_at.strftime('%Y-%m-%d') if p.updated_at else 'N/A'
            ])
            
        csv_content = output.getvalue()
        output.close()
        
        print(f"Emailing Platform Report CSV to {admin_email}...")
        time.sleep(2)
        print(f"Platform Export task complete!")

    return {"status": "success", "email": admin_email}