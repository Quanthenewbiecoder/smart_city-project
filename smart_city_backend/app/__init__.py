from flask import Flask
from app.models.database import db
from app.routes.traffic import traffic_bp
from app.routes.pollution import pollution_bp
from app.routes.waste import waste_bp
from app.routes.metering import metering_bp
from app.routes.dashboard import home_bp  # Add this

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///smart_city.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # Register Blueprints
    app.register_blueprint(traffic_bp, url_prefix="/traffic")
    app.register_blueprint(pollution_bp, url_prefix="/pollution")
    app.register_blueprint(waste_bp, url_prefix="/waste")
    app.register_blueprint(metering_bp, url_prefix="/metering")
    app.register_blueprint(home_bp)  # Register home blueprint

    return app
