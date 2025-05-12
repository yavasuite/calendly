from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS  # <-- Add this
from dotenv import load_dotenv
import os

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
migrate = Migrate()

def create_app(config_name="production"):
    load_dotenv()

    app = Flask(__name__)

    # Load environment-specific configuration
    if config_name == "production":
        app.config.from_object("config.ProductionConfig")
    elif config_name == "development":
        app.config.from_object("config.DevelopmentConfig")
    else:
        app.config.from_object("config.Config")  # fallback/default

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # ✅ Enable CORS globally (do it here)
    CORS(app, supports_credentials=True)

    # Register routes
    from app.routes import register_blueprints
    register_blueprints(app)

    return app
