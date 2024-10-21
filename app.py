from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import date
import csv
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuratie voor de SQLite-database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///records.db'
app.config['UPLOAD_FOLDER'] = './uploads'
db = SQLAlchemy(app)

# Het Record-model, aangepast met 'onderdeel' en 'categorie'
class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    atleet = db.Column(db.String(255), nullable=False)
    geslacht = db.Column(db.String(10), nullable=False)  # Man/Vrouw
    onderdeel = db.Column(db.String(255), nullable=False)  # Onderdeel van de sport
    categorie = db.Column(db.String(50), nullable=False)   # Categorie zoals 'Senioren'
    prestatie = db.Column(db.Float, nullable=False)
    datum = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='in afwachting')  # New status field
    approved_by = db.Column(db.String(100), nullable=True)  

# Initialiseer de database
#@app.before_first_request
#def init_db():
#    db.create_all()

# Route voor de homepage met alle records in afwachting
@app.route('/records')
def records_home():
    records = Record.query.filter_by(status='in afwachting').all()
    return render_template('records_home.html', records=records)

# Route voor goedkeuren van een record
@app.route('/approve_record/<int:record_id>', methods=['POST'])
def approve_record(record_id):
    record = Record.query.get_or_404(record_id)
    record.status = 'approved'
    db.session.commit()
    return redirect('/records')

# Route voor afwijzen van een record
@app.route('/reject_record/<int:record_id>', methods=['POST'])
def reject_record(record_id):
    record = Record.query.get_or_404(record_id)
    record.status = 'rejected'
    db.session.commit()
    return redirect('/records')

# Route voor het toevoegen van een record (handmatige invoer)
@app.route('/add_record', methods=['GET', 'POST'])
def add_record():
    if request.method == 'POST':
        atleet = request.form['atleet']
        geslacht = request.form['geslacht']
        onderdeel = request.form['onderdeel']
        categorie = request.form['categorie']
        prestatie = request.form['prestatie']
        datum = request.form['datum']

        new_record = Record(atleet=atleet, geslacht=geslacht, onderdeel=onderdeel, categorie=categorie, prestatie=float(prestatie), datum=date.fromisoformat(datum), status='in afwachting')

        db.session.add(new_record)
        db.session.commit()

        return redirect(url_for('records_home'))

    return render_template('add_record.html')

# Route voor goedgekeurde records
@app.route('/approved_records')
def approved_records():
    records = Record.query.filter_by(status='approved').all()
    return render_template('approved_records.html', records=records)

# Route voor afgekeurde records
@app.route('/rejected_records')
def rejected_records():
    records = Record.query.filter_by(status='rejected').all()
    return render_template('rejected_records.html', records=records)

# Route voor CSV-upload
@app.route('/upload-csv', methods=['GET', 'POST'])
def upload_csv():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.csv'):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Lees en voeg records toe vanuit de CSV
            with open(filepath, mode='r', encoding='utf-8') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    atleet = row['atleet']
                    geslacht = row['geslacht']
                    onderdeel = row['onderdeel']
                    categorie = row['categorie']
                    prestatie = float(row['prestatie'])
                    datum = date.fromisoformat(row['datum'])

                    new_record = Record(atleet=atleet, geslacht=geslacht, onderdeel=onderdeel, categorie=categorie, prestatie=prestatie, datum=datum, status='in afwachting')

                    db.session.add(new_record)

                db.session.commit()

            return redirect(url_for('upload_csv'))

    return render_template('upload_csv.html')

# Route voor publieke weergave van records die in afwachting zijn
@app.route('/records/publiek')
def show_public_records():
    pending_records = Record.query.filter_by(status='in afwachting').all()

    # Onderverdeel de records op basis van geslacht
    records_man = [r for r in pending_records if r.geslacht == 'man']
    records_vrouw = [r for r in pending_records if r.geslacht == 'vrouw']

    # Sorteer records op onderdeel
    records_man_sorted = sorted(records_man, key=lambda x: x.onderdeel)
    records_vrouw_sorted = sorted(records_vrouw, key=lambda x: x.onderdeel)

    return render_template('public_records.html', records_man=records_man_sorted, records_vrouw=records_vrouw_sorted)

# Hoofdpagina voor records beheer
#@app.route('/records')
#def records_home():
 #   return render_template('records_home.html')


# Start de Flask applicatie
if __name__ == '__main__':
    app.run(debug=True)
