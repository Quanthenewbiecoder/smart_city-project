from flask import Blueprint, jsonify
from app.models.database import db, Traffic, Pollution, Waste, Metering

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard', methods=['GET'])
def get_dashboard_data():
    traffic_data = Traffic.query.all()
    pollution_data = Pollution.query.all()
    waste_data = Waste.query.all()
    metering_data = Metering.query.all()

    response = {
        "traffic": [{"location": t.location, "congestion_level": t.congestion_level} for t in traffic_data],
        "pollution": [{"location": p.location, "air_quality_index": p.air_quality_index} for p in pollution_data],
        "waste": [{"location": w.location, "bin_fill_level": w.bin_fill_level} for w in waste_data],
        "metering": [{"location": m.location, "water_usage": m.water_usage, "energy_usage": m.energy_usage} for m in metering_data],
    }

    return jsonify(response)

from flask import Blueprint

home_bp = Blueprint("home", __name__)

@home_bp.route("/")
def index():
    return "Welcome to the Smart City Dashboard!"
