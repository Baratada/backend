from flask import Blueprint, jsonify, request
from app.models.appointment import Appointment
from app.models.user import User
from app.extensions import db
from datetime import datetime

appoint_bp = Blueprint("appointments", __name__)

# Get all appointments
@appoint_bp.route("", methods=["GET"])
def get_appointments():
    appointments = Appointment.query.all()
    return jsonify([appointment.to_dict() for appointment in appointments])

# Book an appointment
@appoint_bp.route("", methods=["POST"])  # Changed to root route
def book_appointment():
    data = request.json
    patient_id = data.get("patient_id")
    doctor_id = data.get("doctor_id")
    date_str = data.get("appointment_date")

    if not patient_id:
        return jsonify({"error": "Missing patient_id"}), 400
    if not doctor_id:
        return jsonify({"error": "Missing doctor_id"}), 400
    if not date_str:
        return jsonify({"error": "Missing appointment_date"}), 400
    # Validate users
    patient = User.query.get(patient_id)
    doctor = User.query.get(doctor_id)

    if not patient or not doctor or doctor.role != "doctor":
        return jsonify({"error": "Invalid patient or doctor"}), 400

    try:
        date = datetime.fromisoformat(date_str)
    except ValueError:
        return jsonify({"error": "Invalid date format"}), 400

    appointment = Appointment(patient_id=patient_id, doctor_id=doctor_id, appointment_date=date, status="pending", created_at = date.isoformat(), updated_at = date.isoformat())
    db.session.add(appointment)
    db.session.commit()

    return jsonify({"message": "Appointment booked successfully", "appointment": appointment.to_dict()}), 201

# Update appointment status
@appoint_bp.route("/update-status/<int:appointment_id>", methods=["PATCH"])
def update_status(appointment_id):
    data = request.json
    status = data.get("status")

    if status not in ["pending", "confirmed", "canceled"]:
        return jsonify({"error": "Invalid status"}), 400

    appointment = Appointment.query.get(appointment_id)
    if not appointment:
        return jsonify({"error": "Appointment not found"}), 404

    appointment.status = status
    db.session.commit()

    return jsonify({"message": "Appointment status updated", "appointment": appointment.to_dict()})

# Delete an appointment
@appoint_bp.route("/delete/<int:appointment_id>", methods=["DELETE"])
def delete_appointment(appointment_id):
    appointment = Appointment.query.get(appointment_id)
    if not appointment:
        return jsonify({"error": "Appointment not found"}), 404

    db.session.delete(appointment)
    db.session.commit()

    return jsonify({"message": "Appointment deleted successfully"})