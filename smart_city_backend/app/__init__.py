from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from app.models.database import db
import os

# Initialize Migrate
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Load Configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI", "sqlite:///smart_city.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    # Import and Register Blueprints
    from app.routes import (
        traffic, pollution, waste, metering, dashboard, home
    )
    from app.routes.predictions import (
        traffic_prediction, pollution_prediction, waste_prediction, metering_prediction
    )

    # Blueprint registration mapping
    blueprints = [
        (traffic.traffic_bp, "/api/traffic"),
        (pollution.pollution_bp, "/api/pollution"),
        (waste.waste_bp, "/api/waste"),
        (metering.metering_bp, "/api/metering"),
        (dashboard.dashboard_bp, "/dashboard"),
        (home.home_bp, "/api/home"),
        (traffic_prediction.traffic_prediction_bp, "/api/predictions/traffic"),
        (pollution_prediction.pollution_prediction_bp, "/api/predictions/pollution"),
        (waste_prediction.waste_prediction_bp, "/api/predictions/waste"),
        (metering_prediction.metering_prediction_bp, "/api/predictions/metering"),
    ]

    # Register each blueprint
    for bp, prefix in blueprints:
        app.register_blueprint(bp, url_prefix=prefix)

    return app