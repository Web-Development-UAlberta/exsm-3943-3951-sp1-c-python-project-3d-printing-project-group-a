import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DB_URL")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET")
    STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
    DEBUG = os.getenv("FLASK_ENV") == "development"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)