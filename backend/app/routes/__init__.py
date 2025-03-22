from .auth import auth_bp
from .main import main
from .meeting import meeting_bp

def register_blueprints(app):
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(main)
    app.register_blueprint(meeting_bp)