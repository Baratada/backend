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

@user_bp.route('/update-age/<int:user_id>/<int:age>', methods=['PATCH'])
@jwt_required()
def update_age(user_id, age):

    # Validate age input
    if not isinstance(age, int) or age < 0 or age > 120:
        return jsonify({'error': 'Age must be a number between 0 and 120'}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    user.age = age
    db.session.commit()

    return jsonify({'message': 'User age updated successfully', 'user_id': user.id, 'new_age': user.age})

# Get a specific user by ID
@user_bp.route('<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)  # Automatically returns 404 if not found
    return jsonify(user.to_dict())