import random
import numpy as np
from flask import Blueprint, jsonify
from flask_cors import CORS
from sklearn.ensemble import RandomForestRegressor
from app.models.database import db, Traffic, Pollution, Waste, Metering, Location

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')
CORS(dashboard_bp)

def get_real_data():
    """ Fetch real data from the database """
    traffic_data = Traffic.query.order_by(Traffic.id).all()
    pollution_data = Pollution.query.order_by(Pollution.id).all()
    waste_data = Waste.query.order_by(Waste.id).all()
    metering_data = Metering.query.order_by(Metering.id).all()

    return {
        "traffic": [{"location": Location.query.get(t.location_id).name, "congestion_level": t.congestion_level} for t in traffic_data],
        "pollution": [{"location": Location.query.get(p.location_id).name, "air_quality_index": p.air_quality_index} for p in pollution_data],
        "waste": [{"location": Location.query.get(w.location_id).name, "bin_fill_level": w.bin_fill_level} for w in waste_data],
        "metering": [{"location": Location.query.get(m.location_id).name, "water_usage": m.water_usage, "energy_usage": m.energy_usage} for m in metering_data]
    }

@dashboard_bp.route('/', methods=['GET'])
def get_dashboard_data():
    real_data = get_real_data()
    return jsonify(real_data)
