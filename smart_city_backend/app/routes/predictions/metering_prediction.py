import numpy as np
import random
from flask import Blueprint, jsonify
from sklearn.linear_model import LinearRegression
from app.models.database import db, Metering

metering_prediction_bp = Blueprint("metering_prediction", __name__)

def predict_metering_usage(historical_data):
    """ Predicts water and energy usage with seasonal fluctuations """
    ids = np.array([data.id for data in historical_data]).reshape(-1, 1)
    water_usage = np.array([data.water_usage for data in historical_data])

    model = LinearRegression()
    model.fit(ids, water_usage)

    future_ids = np.array([[ids[-1][0] + i] for i in range(1, 4)])
    predicted_water_usage = model.predict(future_ids)

    # Adding seasonal effects (hot days = more water/electricity usage)
    for i in range(len(predicted_water_usage)):
        seasonal_effect = random.choice([-50, 0, 30, 70])  # Cold days (-), heat waves (+)
        predicted_water_usage[i] += seasonal_effect
        predicted_water_usage[i] = max(0, predicted_water_usage[i])  # No negative values

    return {
        "next_periods": [
            {"period": int(future_ids[i][0]), "predicted_water_usage": round(predicted_water_usage[i], 2)}
            for i in range(3)
        ]
    }

@metering_prediction_bp.route("/predict", methods=["GET"])
def get_metering_prediction():
    try:
        historical_data = Metering.query.order_by(Metering.id).all()
        if not historical_data or len(historical_data) < 3:
            return jsonify({"error": "Not enough data for prediction"}), 400

        prediction_result = predict_metering_usage(historical_data)
        return jsonify(prediction_result)

    except Exception as e:
        return jsonify({"error": f"Failed to predict metering usage: {str(e)}"}), 500
