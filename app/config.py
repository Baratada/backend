# app/config.py
import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', "seveneleven")
    JWT_SECRET_KEY = SECRET_KEY
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)
    CORS_ORIGINS = ["http://93.86.64.15"]
    CORS_SUPPORTS_CREDENTIALS = True
    CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
    CORS_ALLOW_HEADERS = ["Content-Type", "Authorization"]
