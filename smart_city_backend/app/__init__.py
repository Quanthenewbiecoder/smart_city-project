from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from app.models.database import db
import os

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///smart_city.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize the database and models
    db.init_app(app)

    migrate.init_app(app, db)  # Initialize Flask-Migrate
    CORS(app)  # Apply CORS globally

    # Register Blueprints
    from app.routes.traffic import traffic_bp
    from app.routes.pollution import pollution_bp
    from app.routes.waste import waste_bp
    from app.routes.metering import metering_bp
    from app.routes.dashboard import dashboard_bp, home_bp  # Import both blueprints

    app.register_blueprint(traffic_bp, url_prefix="/api/traffic")
    app.register_blueprint(pollution_bp, url_prefix="/api/pollution")
    app.register_blueprint(waste_bp, url_prefix="/api/waste")
    app.register_blueprint(metering_bp, url_prefix="/api/metering")
    
    app.register_blueprint(dashboard_bp, url_prefix="/api/Dashboard")  # Register dashboard blueprint
    app.register_blueprint(home_bp)  # Register home blueprint

    return app
