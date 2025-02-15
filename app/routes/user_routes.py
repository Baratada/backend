# app/routes/user_routes.py
from flask import Blueprint, jsonify, abort
from app.models.user import User
from app.extensions import db

user_bp = Blueprint('user', __name__)

# Get all users
@user_bp.route('', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

# Get a specific user by ID
@user_bp.route('<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)  # Automatically returns 404 if not found
    return jsonify(user.to_dict())