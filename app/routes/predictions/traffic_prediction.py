import numpy as np
import random
from flask import Blueprint, jsonify
from sklearn.linear_model import LinearRegression
from app.models.database import db, Traffic

traffic_prediction_bp = Blueprint("traffic_prediction", __name__)

def predict_traffic(historical_data):
    """ Predicts traffic congestion with realistic fluctuations """
    ids = np.array([data.id for data in historical_data]).reshape(-1, 1)
    congestion_levels = np.array([data.congestion_level for data in historical_data])

    # Train the model
    model = LinearRegression()
    model.fit(ids, congestion_levels)

    # Predict for next 3 periods
    future_ids = np.array([[ids[-1][0] + i] for i in range(1, 4)])
    predicted_congestion = model.predict(future_ids)

    # Add random event-based fluctuations
    for i in range(len(predicted_congestion)):
        event_effect = random.choice([-5, 0, 5, 10])  # Simulating events like accidents, rush hour
        predicted_congestion[i] += event_effect
        predicted_congestion[i] = max(0, min(100, predicted_congestion[i]))  # Keep within 0-100%

    return {
        "next_periods": [
            {"period": int(future_ids[i][0]), "predicted_congestion_level": round(predicted_congestion[i], 2)}
            for i in range(3)
        ]
    }

@traffic_prediction_bp.route("/predict", methods=["GET"])
def get_prediction():
    try:
        historical_data = Traffic.query.order_by(Traffic.id).all()
        if not historical_data or len(historical_data) < 3:
            return jsonify({"error": "Not enough data for prediction"}), 400

        prediction_result = predict_traffic(historical_data)
        return jsonify(prediction_result)

    except Exception as e:
        return jsonify({"error": f"Failed to predict traffic congestion: {str(e)}"}), 500
