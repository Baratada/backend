from flask import Blueprint, request, jsonify
import uuid  # Import UUID for generating unique values
from app.extensions import db
from app.models.user import User
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
import datetime

appoint_bp = Blueprint("appointment", __name__)

# Register Route
@appoint_bp.route("/appoint", methods=["POST"])
def appointUser():
    data = request.json
    username = data.get("username")
    role = data.get("role")
    specialization = data.get("specialization")

    # Check if the username already exists
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400

    # Create the new user
    new_user = User(username=username, role=role, specialization=specialization if role == "doctor" else None)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!"}), 201

