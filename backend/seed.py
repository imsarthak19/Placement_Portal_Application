from app import app, db, bcrypt
from application.models import Company


def seed_companies():

    companies = [
        {
            "username": "google",
            "email": "hr@google.com",
            "name": "Google",
            "approved": True,
            "description": "Google is a global technology company specializing in internet-related services and products including search, cloud computing, and advertising technologies.",
            "industry": "Technology",
            "scale": "100,000+ employees",
            "headOffice": "California, USA",
            "website": "https://google.com",
            "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/Google_%22G%22_logo.svg/1920px-Google_%22G%22_logo.svg.png",
            "pocName": "Amit Sharma",
            "pocEmail": "amit@google.com"
        },
        {
            "username": "microsoft",
            "email": "hr@microsoft.com",
            "name": "Microsoft",
            "approved": True,
            "description": "Microsoft develops, licenses, and supports software, services, devices, and solutions worldwide.",
            "industry": "Technology",
            "scale": "100,000+ employees",
            "headOffice": "Redmond, USA",
            "website": "https://microsoft.com",
            "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Microsoft_logo.svg/500px-Microsoft_logo.svg.png",
            "pocName": "Rohit Verma",
            "pocEmail": "rohit@microsoft.com"
        },
    ]

    for data in companies:

        hashed_password = bcrypt.generate_password_hash("company123").decode("utf-8")

        company = Company(
            username=data["username"],
            email=data["email"],
            password=hashed_password,
            name=data["name"],
            approved=data["approved"],
            description=data["description"],
            industry=data["industry"],
            scale=data["scale"],
            headOffice=data["headOffice"],
            website=data["website"],
            logo=data["logo"],
            pocName=data["pocName"],
            pocEmail=data["pocEmail"]
        )

        db.session.add(company)

    db.session.commit()

    print("5 Dummy companies with full data added successfully")


if __name__ == "__main__":
    with app.app_context():
        seed_companies()