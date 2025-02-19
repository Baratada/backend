from app.extensions import db
from .association_tables import user_drugs

class Drugs(db.Model):
    __tablename__ = "drugs"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    prescription = db.Column(db.Boolean, nullable=False, default=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    info = db.Column(db.String(250), default='Speak to your doctor before use of drug.')
    price = db.Column(db.Float, nullable=False, default=0.0)

    users = db.relationship(
        'User', 
        secondary=user_drugs, 
        back_populates='drugs',
        foreign_keys=[user_drugs.c.drug_id, user_drugs.c.user_id]
    )


    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "prescription": self.prescription,
            "stock": self.stock,
            "user_ids": [user.id for user in self.users],
            "info": self.info,
            "price": self.price
        }
