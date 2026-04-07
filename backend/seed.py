from app import app, db, bcrypt
from application.models import Company


def seed_companies():

    companies = [
        {
            "username": "google",
            "email": "hr@google.com",
            "name": "Google",
            "approved": False,
            "industry": "Technology",
            "scale": "Large",
            "headOffice": "California, USA",
            "website": "https://google.com"
        },
        {
            "username": "microsoft",
            "email": "hr@microsoft.com",
            "name": "Microsoft",
            "approved": False,
            "industry": "Technology",
            "scale": "Large",
            "headOffice": "Redmond, USA",
            "website": "https://microsoft.com"
        },
        {
            "username": "amazon",
            "email": "hr@amazon.com",
            "name": "Amazon",
            "approved": True,
            "industry": "Technology",
            "scale": "Large",
            "headOffice": "Seattle, USA",
            "website": "https://amazon.com"
        }
    ]

    for data in companies:

        hashed_password = bcrypt.generate_password_hash("company123").decode("utf-8")

        company = Company(
            username=data["username"],
            email=data["email"],
            password=hashed_password,
            approved=data["approved"],
            name=data["name"],
            industry=data["industry"],
            scale=data["scale"],
            headOffice=data["headOffice"],
            website=data["website"]
        )

        db.session.add(company)

    db.session.commit()

    print("Dummy companies added successfully")


if __name__ == "__main__":
    with app.app_context():
        seed_companies()