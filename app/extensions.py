# app/extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# Initialize extensions
db = SQLAlchemy()  # Database instance


migrate = Migrate()  # Database migrations
jwt = JWTManager()  # JWT authentication
cors = CORS(resources={
    r"/api/*": {
        "origins": ["http://localhost:4200"],
        "methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],

        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True,
        "expose_headers": ["Authorization"],
        "max_age": 600,
        "send_wildcard": True,
        "automatic_options": True
    }
})  # CORS support
