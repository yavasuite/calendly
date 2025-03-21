from flask_jwt_extended import create_access_token
from datetime import timedelta

def generate_access_token(user_id):
    return create_access_token(identity=user_id, expires_delta=timedelta(days=7))