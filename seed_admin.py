from werkzeug.security import generate_password_hash
from app import create_app
from app.extensions import db
from app.models.user import User

# Create the app instance
app = create_app()

def create_admin_and_doctors():
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
                    role=doctor['role'],
                    specialization=doctor['specialization']  # Add the specialization
                )
                
                # Add the doctor to the database
                db.session.add(new_doctor)
                db.session.commit()
                print(f"Doctor user {doctor['username']} created successfully!")
            else:
                print(f"Doctor user {doctor['username']} already exists.")

# Call the function to create the admin and doctors
create_admin_and_doctors()
