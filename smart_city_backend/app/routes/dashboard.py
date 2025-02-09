import random
import numpy as np
from flask import Blueprint, jsonify
from flask_cors import CORS
from sklearn.ensemble import RandomForestRegressor

dashboard_bp = Blueprint('dashboard', __name__)
CORS(dashboard_bp)

def generate_dynamic_data():
    """ Simulates realistic city data using machine learning models """
    # Generate past traffic data (Simulated)
    np.random.seed(42)
    past_traffic = np.array(range(1, 11)).reshape(-1, 1)
    traffic_levels = np.array([12, 22, 33, 29, 45, 48, 58, 62, 67, 75]) 

    # Train a Random Forest Regressor
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(past_traffic, traffic_levels)

    # Predict future traffic levels
    future_traffic = np.array([[11], [12], [13]])
    predicted_traffic = model.predict(future_traffic).tolist()

    return {
        "traffic": [{"location": f"Zone {i+1}", "congestion_level": int(predicted_traffic[i] + random.randint(-3, 3))} for i in range(3)],
        "pollution": [{"location": f"Area {i+1}", "air_quality_index": random.randint(35, 120)} for i in range(3)],
        "waste": [{"location": f"Sector {i+1}", "bin_fill_level": random.randint(10, 95)} for i in range(3)],
        "metering": [{"location": f"District {i+1}", "water_usage": random.randint(550, 2100), "energy_usage": random.randint(1200, 5200)} for i in range(3)]
    }

@dashboard_bp.route('/', methods=['GET'])
def get_dashboard_data():
    simulated_data = generate_dynamic_data()
    return jsonify(simulated_data)
