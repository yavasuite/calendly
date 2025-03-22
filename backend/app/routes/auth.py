from flask import Blueprint, request, jsonify
from app.models.user import User
from app import db
from app.utils.jwt import generate_access_token

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'User')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    if role not in ['User', 'Admin']:
        return jsonify({"error": "Invalid role"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 400

    user = User(email=email, role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    token = generate_access_token(user.id)
    return jsonify({"message": f"{role} registered successfully", "token": token}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        token = generate_access_token(user)
        return jsonify({
            "access_token": token,
            "role": user.role,
            "user_id": user.id
        }), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401
