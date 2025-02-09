import random
import numpy as np
from flask import Blueprint, jsonify, request
from flask_cors import CORS
from app.models.database import db, Traffic, Pollution, Waste, Metering
from sklearn.linear_model import LinearRegression

# Blueprint setup
dashboard_bp = Blueprint('dashboard', __name__)
CORS(dashboard_bp)

def generate_dynamic_data():
    """ Simulates realistic city data using machine learning models """
    # Simulating past data
    past_traffic = np.array(range(1, 11)).reshape(-1, 1)
    traffic_levels = np.array([10, 20, 30, 25, 40, 50, 55, 60, 65, 70])
    
    model = LinearRegression()
    model.fit(past_traffic, traffic_levels)
    future_traffic = np.array([[11], [12], [13]])
    predicted_traffic = model.predict(future_traffic).tolist()
    
    return {
        "traffic": [{"location": f"Zone {i+1}", "congestion_level": int(predicted_traffic[i] + random.randint(-5, 5))} for i in range(3)],
        "pollution": [{"location": f"Area {i+1}", "air_quality_index": random.randint(30, 100)} for i in range(3)],
        "waste": [{"location": f"Sector {i+1}", "bin_fill_level": random.randint(10, 90)} for i in range(3)],
        "metering": [{"location": f"District {i+1}", "water_usage": random.randint(500, 2000), "energy_usage": random.randint(1000, 5000)} for i in range(3)]
    }

@dashboard_bp.route('/dashboard', methods=['GET'])
def get_dashboard_data():
    simulated_data = generate_dynamic_data()
    return jsonify(simulated_data)
