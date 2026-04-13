from app import app, db
from application.models import Drive
from datetime import datetime, timedelta
import random


def seed_drives():

    statuses = ["Unapproved", "Active", "Closed"]
    work_modes = ["Onsite", "Remote", "Hybrid"]
    locations = ["Bangalore", "Hyderabad", "Delhi", "Mumbai", "Pune"]
    roles = [
        "Software Engineer",
        "Data Scientist",
        "Backend Developer",
        "Frontend Developer",
    ]

    drives = []

    for i in range(4):

        drive = Drive(
            company_id=random.choice([1, 2]),

            status=random.choice(statuses),

            title=f"{random.choice(roles)} Hiring Drive",

            description="We are looking for passionate candidates to join our team.",

            eligibility="CGPA > 7.0",

            batch=random.choice([
                "2023,2024",
                "2024",
                "2022,2023,2024"
            ]),

            branches=random.choice([
                "CSE,IT",
                "CSE,IT,ECE",
                "All"
            ]),

            deadline=datetime.now() + timedelta(days=random.randint(5, 30)),

            payScale=random.choice([
                "6 LPA",
                "10 LPA",
                "15 LPA",
                "20 LPA"
            ]),

            location=random.choice(locations),

            workMode=random.choice(work_modes),

            interviewRounds=random.choice([
                "Online Assessment, Technical, HR",
                "Technical, HR",
                "Aptitude, Technical, Managerial, HR"
            ]),

            positions=random.randint(2, 20)
        )

        drives.append(drive)

    db.session.add_all(drives)
    db.session.commit()

    print("Dummy drives added successfully")


if __name__ == "__main__":
    with app.app_context():
        seed_drives()