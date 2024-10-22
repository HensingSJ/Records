from app import db, app

# Zet de applicatiecontext op
with app.app_context():
    db.create_all() 

    admin = User(username='admin', password='admin')
    db.session.add(admin)
    db.session.commit()

print("Database en tabellen aangemaakt.")