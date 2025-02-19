# app/routes/user_routes.py
from flask import Blueprint, jsonify, abort, request
from app.models.user import User
from app.extensions import db
from flask_jwt_extended import jwt_required

user_bp = Blueprint('user', __name__)

# Get all users
@user_bp.route('', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@user_bp.route('/update/<int:user_id>', methods=['PATCH'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.json

    # Update only provided fields
    if 'role' in data:
        user.role = data['role']
    if 'specialization' in data:
        user.specialization = data['specialization']
    if 'age' in data:
        user.age = data['age']

    db.session.commit()
    return jsonify({"message": "User updated successfully", "user": user.to_dict()})
# Get a specific user by ID
@user_bp.route('<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)  # Automatically returns 404 if not found
    return jsonify(user.to_dict())