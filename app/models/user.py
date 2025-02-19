from app.extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from .association_tables import user_drugs



class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False, default="user")
    specialization = db.Column(db.String(80), default="None")
    age = db.Column(db.Integer, default=18)
    
    # Relationships
    drugs = db.relationship(
        'Drugs', 
        secondary=user_drugs, 
        lazy='dynamic',
        back_populates='users',
        foreign_keys=[user_drugs.c.user_id, user_drugs.c.drug_id]
    )


    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "specialization": self.specialization,
            "age": self.age,
            "drugs": [drug.to_dict() for drug in self.drugs] if self.drugs else []


        }

    def __repr__(self):
        return f'<User {self.username}>'
