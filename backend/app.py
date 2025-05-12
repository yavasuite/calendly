import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Load allowed CORS origins from environment variable
cors_origins = os.getenv("CORS_ORIGIN", "")
cors_origin_list = [origin.strip() for origin in cors_origins.split(",") if origin.strip()]

# Apply CORS with credentials support
CORS(app, origins=cors_origin_list, supports_credentials=True)

# Import and register your route blueprints
from app.routes.meeting import meeting_bp
from app.routes.availability import availability_bp
from app.routes.auth import auth_bp  # <- make sure to register auth routes too!

app.register_blueprint(meeting_bp)
app.register_blueprint(availability_bp)
app.register_blueprint(auth_bp)

# Health check or root route
@app.route("/")
def index():
    return "Calendly Clone API is running."
