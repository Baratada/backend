from app.extensions import db

user_drugs = db.Table('user_drugs',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('drug_id', db.Integer, db.ForeignKey('drugs.id'), primary_key=True),
    extend_existing=True
)
