from flask import Blueprint, request, jsonify
from app.models.user import User
from app import db
from app.utils.jwt import generate_access_token

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already exists"}), 400

    user = User(email=data["email"])
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()

    token = generate_access_token(user.id)
    return jsonify({"token": token}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data["email"]).first()

    if user and user.check_password(data["password"]):
        token = generate_access_token(user.id)
        return jsonify({"token": token}), 200

    return jsonify({"error": "Invalid credentials"}), 401
