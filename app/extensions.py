# app/extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# Initialize extensions
db = SQLAlchemy()  # Database instance
migrate = Migrate()  # Database migrations
jwt = JWTManager()  # JWT authentication
cors = CORS()  # CORS support