import os
from flask import Flask
from app.models.database import init_db

# Import Config correctly
from config import Config  # Instead of `from app.config import Config`

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Use the Config class to load the configuration

    init_db(app)  # Initialize the database

    # Import and register blueprints
    from app.routes.traffic import traffic_bp
    from app.routes.pollution import pollution_bp
    from app.routes.waste import waste_bp
    from app.routes.metering import metering_bp
    from app.routes.dashboard import dashboard_bp

    app.register_blueprint(traffic_bp, url_prefix='/traffic')
    app.register_blueprint(pollution_bp, url_prefix='/pollution')
    app.register_blueprint(waste_bp, url_prefix='/waste')
    app.register_blueprint(metering_bp, url_prefix='/metering')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')

    return app
