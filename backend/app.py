from flask import Flask
from flask_bcrypt import Bcrypt
from application.database import db
from application.models import User
from config import Config

# Hve added all the configurations in a separate file for better management and security.

app = Flask(__name__)
app.config.from_object(Config)

bcrypt = Bcrypt(app)
db.init_app(app)

with app.app_context():
    db.create_all()
    
    # Programmatically create the manager if it doesn't exist, will add try block later for better production code
    admin_user = User.query.filter_by(username=app.config['ADMIN_USERNAME']).first()

    if not admin_user:
        hashed_password = bcrypt.generate_password_hash(app.config['ADMIN_PASSWORD']).decode('utf-8')
        admin_user = User(
            username=app.config['ADMIN_USERNAME'],
            email=app.config['ADMIN_EMAIL'],
            password=hashed_password,
            name=app.config['ADMIN_NAME'],
            type='admin'
        )

        db.session.add(admin_user)
        db.session.commit()
        print('Manager Created Successfully, now you can login withe crednentials')
    else:
        print('Manager Already Exists, You can directly login with the credentials')

from application.controllers import *

if __name__ == "__main__":
    app.run(debug=True)