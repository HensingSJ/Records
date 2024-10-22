from app import db, User, app  # Make sure to import 'app'
from werkzeug.security import generate_password_hash

with app.app_context():  # Initialize app context
    new_user = User(username='admin', password=generate_password_hash('admin', method='pbkdf2:sha256'))
    db.session.add(new_user)
    db.session.commit()

print("Admin user created successfully!")