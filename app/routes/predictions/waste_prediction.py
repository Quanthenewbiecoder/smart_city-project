import numpy as np
import random
from flask import Blueprint, jsonify
from sklearn.linear_model import LinearRegression
from app.models.database import db, Waste

waste_prediction_bp = Blueprint("waste_prediction", __name__)

def predict_waste(historical_data):
    """ Predicts waste bin fill levels based on city-wide factors """
    ids = np.array([data.id for data in historical_data]).reshape(-1, 1)
    bin_fill_levels = np.array([data.bin_fill_level for data in historical_data])

    model = LinearRegression()
    model.fit(ids, bin_fill_levels)

    future_ids = np.array([[ids[-1][0] + i] for i in range(1, 4)])
    predicted_waste = model.predict(future_ids)

    # Simulating city-wide effects (holidays, festivals, waste collection)
    for i in range(len(predicted_waste)):
        event_effect = random.choice([-20, -10, 0, 10, 20])  # Holidays (-), events (+)
        predicted_waste[i] += event_effect
        predicted_waste[i] = max(0, predicted_waste[i])  # Prevent negative waste

    return {
        "next_periods": [
            {"period": int(future_ids[i][0]), "predicted_bin_fill_level": round(predicted_waste[i], 2)}
            for i in range(3)
        ]
    }

@waste_prediction_bp.route("/predict", methods=["GET"])
def get_waste_prediction():
    try:
        historical_data = Waste.query.order_by(Waste.id).all()
        if not historical_data or len(historical_data) < 3:
            return jsonify({"error": "Not enough data for prediction"}), 400

        prediction_result = predict_waste(historical_data)
        return jsonify(prediction_result)

    except Exception as e:
        return jsonify({"error": f"Failed to predict waste generation: {str(e)}"}), 500
