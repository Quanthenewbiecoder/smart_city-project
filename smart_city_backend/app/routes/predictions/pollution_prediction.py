import numpy as np
import random
from flask import Blueprint, jsonify
from sklearn.linear_model import LinearRegression
from app.models.database import db, Pollution

pollution_prediction_bp = Blueprint("pollution_prediction", __name__)

def predict_air_quality(historical_data):
    """ Predicts air quality with weather-based randomization """
    ids = np.array([data.id for data in historical_data]).reshape(-1, 1)
    air_quality_index = np.array([data.air_quality_index for data in historical_data])

    model = LinearRegression()
    model.fit(ids, air_quality_index)

    future_ids = np.array([[ids[-1][0] + i] for i in range(1, 4)])
    predicted_air_quality = model.predict(future_ids)

    # Simulate real-world pollution effects
    for i in range(len(predicted_air_quality)):
        weather_effect = random.choice([-10, 0, 5, 15])  # Rain, storms, high winds
        predicted_air_quality[i] += weather_effect
        predicted_air_quality[i] = max(0, predicted_air_quality[i])  # No negative pollution

    return {
        "next_periods": [
            {"period": int(future_ids[i][0]), "predicted_air_quality_index": round(predicted_air_quality[i], 2)}
            for i in range(3)
        ]
    }

@pollution_prediction_bp.route("/predict", methods=["GET"])
def get_pollution_prediction():
    try:
        historical_data = Pollution.query.order_by(Pollution.id).all()
        if not historical_data or len(historical_data) < 3:
            return jsonify({"error": "Not enough data for prediction"}), 400

        prediction_result = predict_air_quality(historical_data)
        return jsonify(prediction_result)

    except Exception as e:
        return jsonify({"error": f"Failed to predict air quality: {str(e)}"}), 500
