from flask import Blueprint, request, jsonify
import uuid  # Import UUID for generating unique values
from app.extensions import db
from app.models.user import User
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
import datetime

auth_bp = Blueprint("auth", __name__)

# Register Route
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    role = data.get("role")
    specialization = data.get("specialization")

    # Check if the username already exists
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400

    # Create the new user
    new_user = User(username=username, role=role, specialization=specialization if role == "doctor" else None)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!"}), 201

# Login Route
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    # Find the user by username
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    # Create the JWT access token and refresh token
    access_token = create_access_token(identity=user.id, expires_delta=datetime.timedelta(days=7))  # Expires in 7 days
    refresh_token = create_refresh_token(identity=user.id)  # Refresh token doesn't expire by default
    
    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "role": user.role,
        "user_id": user.id
    }), 200


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)  # This ensures only a valid refresh token can be used
def refresh():
    # Get the user identity from the refresh token
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user["id"], expires_delta=datetime.timedelta(days=7))  # Expires in 15 minutes
    
    return jsonify({
        "access_token": access_token
    }), 200

