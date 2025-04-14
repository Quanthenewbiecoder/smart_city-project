import random
import numpy as np
from flask import Blueprint, jsonify
from flask_cors import CORS
from app.models.database import db, Traffic, Pollution, Waste, Metering, Location
from app.routes.predictions.traffic_prediction import predict_traffic
from app.routes.predictions.pollution_prediction import predict_air_quality
from app.routes.predictions.waste_prediction import predict_waste
from app.routes.predictions.metering_prediction import predict_metering_usage

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')
CORS(dashboard_bp)

def get_latest_data():
    """ Fetches only the latest real-time data from the database, avoiding excessive old data. """
    try:
        def get_latest_entries(model):
            return model.query.order_by(model.id.desc()).limit(5).all()  # Only fetch the latest 5 entries

        def get_location_name(location_id):
            location = Location.query.get(location_id)
            return location.name if location else "Unknown Location"

        return {
            "traffic": [{"location": get_location_name(t.location_id), "congestion_level": t.congestion_level} for t in get_latest_entries(Traffic)],
            "pollution": [{"location": get_location_name(p.location_id), "air_quality_index": p.air_quality_index} for p in get_latest_entries(Pollution)],
            "waste": [{"location": get_location_name(w.location_id), "bin_fill_level": w.bin_fill_level} for w in get_latest_entries(Waste)],
            "metering": [{"location": get_location_name(m.location_id), "water_usage": m.water_usage, "energy_usage": m.energy_usage} for m in get_latest_entries(Metering)]
        }

    except Exception as e:
        return {"error": f"Failed to retrieve dashboard data: {str(e)}"}

@dashboard_bp.route('/', methods=['GET'])
def get_dashboard_data():
    """ API endpoint to get real-time dashboard data with limited entries. """
    data = get_latest_data()
    return jsonify(data)
