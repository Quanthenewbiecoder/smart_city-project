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

def get_real_data():
    """ Fetches the latest real-time data from the database. """
    try:
        traffic_data = Traffic.query.order_by(Traffic.id).all()
        pollution_data = Pollution.query.order_by(Pollution.id).all()
        waste_data = Waste.query.order_by(Waste.id).all()
        metering_data = Metering.query.order_by(Metering.id).all()

        def get_location_name(location_id):
            location = Location.query.get(location_id)
            return location.name if location else "Unknown Location"

        return {
            "traffic": [{"location": get_location_name(t.location_id), "congestion_level": t.congestion_level} for t in traffic_data],
            "pollution": [{"location": get_location_name(p.location_id), "air_quality_index": p.air_quality_index} for p in pollution_data],
            "waste": [{"location": get_location_name(w.location_id), "bin_fill_level": w.bin_fill_level} for w in waste_data],
            "metering": [{"location": get_location_name(m.location_id), "water_usage": m.water_usage, "energy_usage": m.energy_usage} for m in metering_data]
        }

    except Exception as e:
        return {"error": f"Failed to retrieve dashboard data: {str(e)}"}

@dashboard_bp.route('/', methods=['GET'])
def get_dashboard_data():
    """ API endpoint to get real-time dashboard data. """
    data = get_real_data()
    return jsonify(data)
