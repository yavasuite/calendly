import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")  # used for Flask sessions & JWTs
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
