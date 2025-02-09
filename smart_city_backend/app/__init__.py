from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from app.models.database import db
import os

# Initialize Migrate and CORS
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Database Configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///smart_city.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    # Import and Register Blueprints
    from app.routes.traffic import traffic_bp
    from app.routes.pollution import pollution_bp
    from app.routes.waste import waste_bp
    from app.routes.metering import metering_bp
    from app.routes.dashboard import dashboard_bp  # Ensure this is correct
    from app.routes.home import home_bp  

    # Register Blueprints with their respective URL prefixes
    blueprints = [
        (traffic_bp, "/api/traffic"),
        (pollution_bp, "/api/pollution"),
        (waste_bp, "/api/waste"),
        (metering_bp, "/api/metering"),
        (dashboard_bp, "/dashboard"),  # Registered at '/dashboard'
        (home_bp, "/api/home"),
    ]

    # Register each blueprint
    for bp, prefix in blueprints:
        app.register_blueprint(bp, url_prefix=prefix)

    return app
