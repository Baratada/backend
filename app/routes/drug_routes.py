# app/routes/user_routes.py
from flask import Blueprint, jsonify, abort, request
from app.models.drugs import Drugs
from app.extensions import db
from flask_jwt_extended import jwt_required

drug_bp = Blueprint('drugs', __name__)

# Get all drugs with optional search
@drug_bp.route('', methods=['GET'])
def get_drugs():
    search_term = request.args.get('search')
    if search_term:
        drugs = Drugs.query.filter(Drugs.name.ilike(f'%{search_term}%')).all()
    else:
        drugs = Drugs.query.all()
    return jsonify([drug.to_dict() for drug in drugs])



@drug_bp.route('<int:drug_id>', methods=['GET'])
def get_drug(drug_id):
    user = Drugs.query.get_or_404(drug_id)  # Automatically returns 404 if not found
    return jsonify(user.to_dict())

@drug_bp.route('/update/<int:drug_id>', methods=['PATCH'])
@jwt_required()
def update_drug(drug_id):

    drug = Drugs.query.get(drug_id)
    if not drug:
        return jsonify({"error": "Drug not found"}), 404

    data = request.json

    # Update only provided fields
    if 'price' in data:
        drug.price = data['price']
    if 'info' in data:
        drug.info = data['info']
    if 'stock' in data:
        drug.stock += data['stock']

    db.session.commit()
    return jsonify({"message": "User updated successfully", "user": drug.to_dict()})

@drug_bp.route('/delete/<int:drug_id>', methods=['DELETE'])
@jwt_required()
def delete_drug(drug_id):
    drug = Drugs.query.get(drug_id)
    if not drug:
        return jsonify({"error": "Drug not found"}), 404
    db.session.delete(drug)
    db.session.commit()
    return jsonify({"message": "Drug deleted successfully"}), 200

@drug_bp.route('', methods=['POST'])
@jwt_required()
def add_drug():
    data = request.json
    if not all(k in data for k in ['name', 'price', 'prescription', 'info', 'stock']):
        return jsonify({"error": "Missing fields"}), 400

    drug = Drugs(
        name=data['name'], 
        price=data['price'], 
        prescription=data['prescription'], 
        info=data['info'], 
        stock=data['stock']  # Explicitly set stock
    )

    db.session.add(drug)
    db.session.commit()
    return jsonify({"message": "Drug added successfully", "drug": drug.to_dict()}), 201
