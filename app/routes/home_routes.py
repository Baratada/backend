# backend/app/routes/home_routes.py

from flask import Blueprint, render_template

home_bp = Blueprint('home_bp', __name__)

# Homepage route
@home_bp.route('/')
def home():
    return render_template('home.html')
