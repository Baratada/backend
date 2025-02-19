# app/routes/user_routes.py
from flask import Blueprint, jsonify, abort, request
from app.models.drugs import Drugs
from app.extensions import db

drug_bp = Blueprint('drugs', __name__)

# Get all users
@drug_bp.route('', methods=['GET'])
def get_drugs():
    drugs = Drugs.query.all()
    return jsonify([drug.to_dict() for drug in drugs])


@drug_bp.route('<int:drug_id>', methods=['GET'])
def get_drug(drug_id):
    user = Drugs.query.get_or_404(drug_id)  # Automatically returns 404 if not found
    return jsonify(user.to_dict())
