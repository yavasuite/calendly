from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.utils.jwt import role_required

main = Blueprint('main', __name__)

@main.route("/")
def home():
    return {"message": "Production Flask is alive"}

@main.route("/admin", methods=["GET"])
@jwt_required()
@role_required("Admin")
def admin_only():
    return {"message": "You are an Admin"}