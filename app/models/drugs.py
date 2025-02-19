from app.extensions import db
from .association_tables import user_drugs

class Drugs(db.Model):
    __tablename__ = "drugs"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    prescription = db.Column(db.Boolean, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)

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
            "user_ids": [user.id for user in self.users]
        }
