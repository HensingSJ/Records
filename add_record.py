from app import db, Record, app
from datetime import date

# Zet de applicatiecontext op om database-acties uit te voeren
with app.app_context():
    # Maak een nieuw record aan
    record1 = Record(atleet="Usain Bolt", geslacht="Man", onderdeel="100m", categorie="Sen M", prestatie=9.58, datum=date(2009, 8, 16), status='in afwachting')
    record2 = Record(atleet="Sjoerd Hensing", geslacht="man", onderdeel="Hoogspringen", categorie="Sen M", prestatie=2.00, datum=date(2008, 6, 10), status='in afwachting')


    # Voeg het record toe aan de database
    db.session.add(record1)
    db.session.commit()  # Bevestig de wijzigingen in de database

    print("Record toegevoegd.")