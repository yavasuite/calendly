from flask_jwt_extended import create_access_token, get_jwt, verify_jwt_in_request
from datetime import timedelta
from functools import wraps
from flask import jsonify

def generate_access_token(user):
    # Include role in JWT payload
    additional_claims = {"role": user.role}
    return create_access_token(
        identity=user.id,
        additional_claims=additional_claims,
        expires_delta=timedelta(days=7)
    )

def role_required(required_role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get("role") != required_role:
                return jsonify(msg="Forbidden: Insufficient poermissions"), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator