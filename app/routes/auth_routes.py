from flask import Blueprint, request, jsonify
import uuid
from app.extensions import db
from app.models.user import User
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from datetime import datetime
from datetime import timedelta
auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")
    role = data.get("role")
    specialization = data.get("specialization")
    birth_date = datetime.strptime(data["birth_date"], "%Y-%m-%d") if "birth_date" in data else None
    
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400

    new_user = User(
        username=username,
        birth_date=birth_date,
        email=email,
        role=role,
        specialization=specialization
    )
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity={"id": user.id, "role": user.role}, expires_delta=timedelta(days=7))

    refresh_token = create_refresh_token(identity=user.id)

    return jsonify({
        "access_token": access_token.decode('utf-8') if isinstance(access_token, bytes) else access_token,
        "refresh_token": refresh_token.decode('utf-8') if isinstance(refresh_token, bytes) else refresh_token,
        "role": user.role,
        "user_id": user.id
    }), 200

@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user["id"], expires_delta=datetime.timedelta(days=7))
    
    return jsonify({
        "access_token": access_token
    }), 200
