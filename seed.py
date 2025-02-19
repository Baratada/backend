from werkzeug.security import generate_password_hash
from datetime import datetime
from sqlalchemy import or_

from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.drugs import Drugs
from app.models.appointment import Appointment



# Create the app instance
app = create_app()

def seed_data():

    with app.app_context():  # Use app context for database interactions
        # Create admin user
        admin_user = User.query.filter_by(username='admin').first()
        
        # Check if the admin user already exists
        if not admin_user:
            # Create a new admin user with a hashed password
            hashed_password = generate_password_hash('adminpassword')  # Hash the password
            admin_user = User(
                username='admin',
                password_hash=hashed_password,  # Store the hashed password
                email='admin@hospital.com',
                role='admin'
            )

            
            # Add the user to the database
            db.session.add(admin_user)
            db.session.commit()
            print("Admin user created successfully!")
        else:
            print("Admin user already exists.")
        
        # Add doctor users
        doctor_users = [
            {'username': 'doctor1', 'password': 'doctorpassword1', 'role': 'doctor', 'specialization': 'Cardiology'},
            {'username': 'doctor2', 'password': 'doctorpassword2', 'role': 'doctor', 'specialization': 'Neurology'},
            {'username': 'doctor3', 'password': 'doctorpassword3', 'role': 'doctor', 'specialization': 'Pediatrics'}
        ]
        
        for doctor in doctor_users:
            existing_doctor = User.query.filter_by(username=doctor['username']).first()
            
            if not existing_doctor:
                hashed_password = generate_password_hash(doctor['password'])  # Hash the password
                new_doctor = User(
                    username=doctor['username'],
                    password_hash=hashed_password,  # Store the hashed password
                    email=f"{doctor['username']}@hospital.com",
                    role=doctor['role'],
                    specialization=doctor['specialization']  # Add the specialization
                )

                
                # Add the doctor to the database
                db.session.add(new_doctor)
                db.session.commit()
        print(f"Doctor user {doctor['username']} created successfully!")

        # Create sample drugs if they don't exist
        drugs_to_create = [
            ('Aspirin', False, 100),
            ('Ibuprofen', False, 50),
            ('Amoxicillin', True, 30),
            ('Paracetamol', False, 200),
            ('Lisinopril', True, 40),
            ('Metformin', True, 60),
            ('Atorvastatin', True, 35),
            ('Levothyroxine', True, 25),
            ('Omeprazole', False, 80),
            ('Albuterol', True, 45)
        ]
        
        created_count = 0
        for name, prescription, stock in drugs_to_create:
            existing_drug = Drugs.query.filter_by(name=name).first()
            if not existing_drug:
                drug = Drugs(name=name, prescription=prescription, stock=stock)
                db.session.add(drug)
                created_count += 1
        db.session.commit()
        print(f"Created {created_count} new drugs. {len(drugs_to_create) - created_count} already existed.")


        # Create basic users with associated drugs
        basic_users = [
            {'username': 'user1', 'password': 'userpassword1', 'role': 'user'},
            {'username': 'user2', 'password': 'userpassword2', 'role': 'user'}
        ]
        
        for basic_user in basic_users:
            existing_user = User.query.filter_by(username=basic_user['username']).first()
            
            if not existing_user:
                hashed_password = generate_password_hash(basic_user['password'])
                new_user = User(
                    username=basic_user['username'],
                    password_hash=hashed_password,
                    email=f"{basic_user['username']}@hospital.com",
                    role=basic_user['role']
                )

                db.session.add(new_user)
                db.session.commit()
                
                # Associate drugs with basic users
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


# Call the function to create the admin and doctors
seed_data()
