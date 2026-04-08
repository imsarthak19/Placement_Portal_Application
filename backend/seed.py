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
        {
            "username": "amazon",
            "email": "hr@amazon.com",
            "name": "Amazon",
            "approved": True,
            "description": "Amazon is a multinational technology company focusing on e-commerce, cloud computing, digital streaming, and artificial intelligence.",
            "industry": "Technology",
            "scale": "100,000+ employees",
            "headOffice": "Seattle, USA",
            "website": "https://amazon.com",
            "logo": "https://upload.wikimedia.org/wikipedia/commons/d/de/Amazon_icon.png",
            "pocName": "Neha Kapoor",
            "pocEmail": "neha@amazon.com"
        },
        {
            "username": "flipkart",
            "email": "hr@flipkart.com",
            "name": "Flipkart",
            "approved": True,
            "description": "Flipkart is one of India's leading e-commerce platforms, offering a wide range of products across categories.",
            "industry": "E-commerce",
            "scale": "100,000+ employees",
            "headOffice": "Bangalore, India",
            "website": "https://flipkart.com",
            "logo": "https://i.pinimg.com/736x/aa/70/8d/aa708d1f97a04f6f5a208213f89e1e67.jpg",
            "pocName": "Ankit Singh",
            "pocEmail": "ankit@flipkart.com"
        },
        {
            "username": "tcs",
            "email": "hr@tcs.com",
            "name": "TCS",
            "approved": True,
            "description": "Tata Consultancy Services is an Indian multinational IT services and consulting company.",
            "industry": "IT Services",
            "scale": "100,000+ employees",
            "headOffice": "Mumbai, India",
            "website": "https://tcs.com",
            "logo": "https://logo.clearbit.com/tcs.com",
            "pocName": "Priya Nair",
            "pocEmail": "priya@tcs.com"
        }
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