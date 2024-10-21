from app import db, app

# Zet de applicatiecontext op
with app.app_context():
    db.create_all() 

print("Database en tabellen aangemaakt.")