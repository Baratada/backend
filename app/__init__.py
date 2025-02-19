# app/__init__.py
from flask import Flask
from .config import Config

from .extensions import db, migrate, jwt, cors  # Import extensions


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Load configuration

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)

    # Import models after db initialization
    from app.models.user import User
    from app.models.appointment import Appointment
    from app.models.drugs import Drugs

    # Register blueprints (routes)
    register_blueprints(app)
    
    return app


def register_blueprints(app):
    from app.routes.home_routes import home_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.admin_routes import admin_bp  # Import the new admin routes blueprint
    from app.routes.user_routes import user_bp  # Import user blueprint instead of doctor routes
    from app.routes.appointment_routes import appoint_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")  # Register the admin blueprint
    app.register_blueprint(user_bp, url_prefix="/api/users")  # Register the user blueprint
    app.register_blueprint(appoint_bp, url_prefix="/api/appointments")  # Register the appointment blueprint
