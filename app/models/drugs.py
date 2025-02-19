from app.extensions import db

user_drugs = db.Table('user_drugs',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('drug_id', db.Integer, db.ForeignKey('drugs.id'), primary_key=True)
)

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
        overlaps="associated_drugs,users"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "prescription": self.prescription,
            "stock": self.stock,
            "user_ids": [user.id for user in self.users]
        }
