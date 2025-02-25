from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity, JWTManager

admin_bp = Blueprint("admin", __name__)
jwt = JWTManager()

# Configure JWT identity and user loaders
@jwt.user_identity_loader
def user_identity_lookup(user):
    return {"sub": str(user.id)}  # Ensure 'ub' is a string

@jwt.user_lookup_loader
def user_lookup_callback(jwt_data):
    identity = jwt_data["sub"]
    return User.query.get(identity["id"])  # Match the token structure

# Function to get the current user
def get_current_user():
    identity = get_jwt_identity()
    print("JWT Identity:", identity)  # Debugging
    if isinstance(identity, dict):
        user_id = identity.get("id")
    else:
        user_id = identity  # Fallback for string identity
    return User.query.get(user_id)

@admin_bp.route('/admin-dashboard')
@jwt_required()
def admin_dashboard():
    user = get_current_user()
    if not user or not user.is_admin():
        return jsonify({"message": "Access denied"}), 403
    
    users = User.query.all()  # Get all users from the database
    print("JWT Token's 'ub' claim:", get_jwt_identity())  # Log the 'ub' claim
    return jsonify([{
        'id': u.id,
        'username': u.username,
        'role': u.role,
        'pecialization': u.specialization
    } for u in users])


@admin_bp.route('/delete-user/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    try:
        user = get_current_user()
        print("Current User:", user)  # Debugging
        if not user or not user.is_admin():
            return jsonify({"message": "Access denied"}), 403

        user_to_delete = User.query.get_or_404(user_id)
        db.session.delete(user_to_delete)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"})
    except Exception as e:
        print("Error:", str(e))  # Debugging
        return jsonify({"error": "An error occurred"}), 500
    
@admin_bp.route('/update-role/<int:user_id>', methods=['PATCH'])
@jwt_required()
def update_user_role(user_id):
    try:
        user = get_current_user()
        if not user or not user.is_admin():
            return jsonify({"message": "Access denied"}), 403
        
        # Fetch user to update
        user_to_update = User.query.get_or_404(user_id)
        
        # Get new role from request
        data = request.json
        new_role = data.get('role')
        if not new_role:
            return jsonify({"error": "Role is required"}), 400

        # Validate the role (optional)
        if new_role not in ['admin', 'user', 'doctor']:
            return jsonify({"error": "Invalid role"}), 400

        # Update the role
        user_to_update.role = new_role
        db.session.commit()

        return jsonify({"message": "User role updated successfully", "user": user_to_update.to_dict()})

    except Exception as e:
        print("Error:", str(e))  # Debugging
        return jsonify({"error": "An error occurred"}), 500


@admin_bp.route('/update-specialization/<int:user_id>', methods=['PATCH'])
@jwt_required()
def update_doctor_specialization(user_id):
    try:
        user = get_current_user()
        if not user or not user.is_admin():
            return jsonify({"message": "Access denied"}), 403

        # Fetch the user to update
        doctor_to_update = User.query.get_or_404(user_id)

        # Check if the user is a doctor
        if doctor_to_update.role != 'doctor':
            return jsonify({"error": "User is not a doctor"}), 400
        
        # Get new specialization from request
        data = request.json
        new_specialization = data.get('specialization')
        if not new_specialization:
            return jsonify({"error": "Specialization is required"}), 400

        # Update the specialization
        doctor_to_update.specialization = new_specialization
        db.session.commit()

        return jsonify({"message": "Doctor's specialization updated successfully", "user": doctor_to_update.to_dict()})

    except Exception as e:
        print("Error:", str(e))  # Debugging
        return jsonify({"error": "An error occurred"}), 500
