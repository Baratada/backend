from werkzeug.security import generate_password_hash
from datetime import datetime
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.drugs import Drugs
from app.models.appointment import Appointment

app = create_app()

def seed_data():

    with app.app_context():
        admin_user = User.query.filter_by(username='admin').first()
        
        if not admin_user:
            hashed_password = generate_password_hash('adminpassword')
            admin_user = User(
                username='admin',
                password_hash=hashed_password,
                email='admin@hospital.com',
                role='admin',
                birth_date=datetime(1985, 5, 15)
            )
            db.session.add(admin_user)
            db.session.commit()
            print("Admin user created successfully!")
        else:
            print("Admin user already exists.")
        
        doctor_users = [
            {'username': 'dr_john_smith', 'password': 'doctorpassword1', 'role': 'doctor', 'specialization': 'Cardiology', 'birth_date': datetime(1975, 3, 20)},
            {'username': 'dr_susan_jones', 'password': 'doctorpassword2', 'role': 'doctor', 'specialization': 'Neurology', 'birth_date': datetime(1980, 7, 25)},
            {'username': 'dr_stephen_morris', 'password': 'doctorpassword3', 'role': 'doctor', 'specialization': 'Pediatrics', 'birth_date': datetime(1978, 11, 10)}
        ]
        
        for doctor in doctor_users:
            existing_doctor = User.query.filter_by(username=doctor['username']).first()
            
            if not existing_doctor:
                hashed_password = generate_password_hash(doctor['password'])
                new_doctor = User(
                    username=doctor['username'],
                    password_hash=hashed_password,
                    email=f"{doctor['username']}@hospital.com",
                    role=doctor['role'],
                    specialization=doctor['specialization'],
                    birth_date=doctor['birth_date']
                )
                db.session.add(new_doctor)
                db.session.commit()
                print(f"Doctor {doctor['username']} created successfully!")
            else:
                print(f"Doctor {doctor['username']} already exists.")

        drugs_to_create = [
            ('Aspirin', False, 100, 'Pain reliever', 10.0),
            ('Ibuprofen', False, 50, 'Anti-inflammatory', 5.0),
            ('Amoxicillin', True, 30, 'Antibiotic', 15.0),
            ('Paracetamol', False, 200, 'Pain reliever', 8.0),
            ('Lisinopril', True, 40, 'Blood pressure medication', 20.0),
            ('Metformin', True, 60, 'Diabetes medication', 12.0),
            ('Atorvastatin', True, 35, 'Cholesterol medication', 18.0),
            ('Levothyroxine', True, 25, 'Thyroid medication', 22.0),
            ('Omeprazole', False, 80, 'Acid reducer', 14.0),
            ('Albuterol', True, 45, 'Asthma medication', 25.0),
            ('Ciprofloxacin', True, 60, 'Antibiotic', 18.0),
            ('Furosemide', True, 40, 'Diuretic', 15.0),
            ('Hydrochlorothiazide', True, 70, 'Blood pressure medication', 12.0),
            ('Fluoxetine', True, 90, 'Antidepressant', 25.0),
            ('Cetirizine', False, 150, 'Antihistamine', 8.0),
            ('Prednisone', True, 30, 'Steroid', 28.0),
            ('Naproxen', False, 100, 'Pain reliever', 11.0),
            ('Tamsulosin', True, 40, 'Prostate medication', 22.0),
            ('Doxycycline', True, 60, 'Antibiotic', 19.0),
            ('Clopidogrel', True, 50, 'Antiplatelet', 27.0),
            ('Fentanyl', True, 25, 'Pain reliever', 50.0),
            ('Gabapentin', True, 75, 'Neuropathy medication', 20.0),
            ('Zolpidem', True, 45, 'Sleep aid', 15.0),
            ('Hydrocodone', True, 60, 'Pain reliever', 30.0),
            ('Diazepam', True, 40, 'Anxiety medication', 18.0),
            ('Citalopram', True, 90, 'Antidepressant', 21.0)
        ]

        created_count = 0
        
        for name, prescription, stock, info, price in drugs_to_create:
            existing_drug = Drugs.query.filter_by(name=name).first()
            if not existing_drug:
                drug = Drugs(name=name, prescription=prescription, stock=stock, info=info, price=price)
                db.session.add(drug)
                created_count += 1
        db.session.commit()
        print(f"Created {created_count} new drugs. {len(drugs_to_create) - created_count} already existed.")

        basic_users = [
            {'username': 'user1', 'password': 'userpassword1', 'role': 'user', 'birth_date': datetime(1990, 8, 10)},
            {'username': 'user2', 'password': 'userpassword2', 'role': 'user', 'birth_date': datetime(1992, 6, 15)}
        ]
        
        for basic_user in basic_users:
            existing_user = User.query.filter_by(username=basic_user['username']).first()
            
            if not existing_user:
                hashed_password = generate_password_hash(basic_user['password'])
                new_user = User(
                    username=basic_user['username'],
                    password_hash=hashed_password,
                    email=f"{basic_user['username']}@hospital.com",
                    role=basic_user['role'],
                    birth_date=basic_user['birth_date']
                )

                db.session.add(new_user)
                db.session.commit()
                
                if basic_user['username'] == 'user1':
                    aspirin = Drugs.query.filter_by(name='Aspirin').first()
                    amoxicillin = Drugs.query.filter_by(name='Amoxicillin').first()
                    if aspirin:
                        new_user.drugs.append(aspirin)
                    if amoxicillin:
                        new_user.drugs.append(amoxicillin)
                elif basic_user['username'] == 'user2':
                    ibuprofen = Drugs.query.filter_by(name='Ibuprofen').first()
                    paracetamol = Drugs.query.filter_by(name='Paracetamol').first()
                    if ibuprofen:
                        new_user.drugs.append(ibuprofen)
                    if paracetamol:
                        new_user.drugs.append(paracetamol)

                
                db.session.commit()
                print(f"Basic user {basic_user['username']} created with associated drugs!")
            else:
                print(f"Basic user {basic_user['username']} already exists.")

seed_data()
