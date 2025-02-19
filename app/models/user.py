from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import get_jwt_identity
from app.models.drugs import user_drugs


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    email = db.Column(db.String(120), nullable=False, default="test@test.com")
    role = db.Column(db.String(50), nullable=False, default='user')
    specialization = db.Column(db.String(100), nullable=True)
    age = db.Column(db.Integer, default=18)
    description = db.Column(db.String(500), nullable=True)
    
    drugs = db.relationship('Drugs', secondary=user_drugs, backref=db.backref('users', lazy='dynamic'))



    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == "admin"

    def to_dict(self):
        return {
            'description': self.description
        }