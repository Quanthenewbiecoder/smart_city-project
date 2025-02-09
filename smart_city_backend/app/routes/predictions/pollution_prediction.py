import numpy as np
from flask import Blueprint, jsonify
from sklearn.linear_model import LinearRegression
from app.models.database import db, Pollution

pollution_prediction_bp = Blueprint("pollution_prediction", __name__)

def predict_air_quality(historical_data):
    # Extract historical data
    ids = np.array([data.id for data in historical_data]).reshape(-1, 1)
    air_quality_index = np.array([data.air_quality_index for data in historical_data])

    # Train the model
    model = LinearRegression()
    model.fit(ids, air_quality_index)

    # Predict for the next 3 periods
    future_ids = np.array([[ids[-1][0] + 1], [ids[-1][0] + 2], [ids[-1][0] + 3]])
    predicted_air_quality = model.predict(future_ids).tolist()

    return {
        "next_periods": [
            {"period": int(future_ids[i][0]), "predicted_air_quality_index": round(predicted_air_quality[i], 2)}
            for i in range(3)
        ]
    }

# Define an API endpoint
@pollution_prediction_bp.route("/predict", methods=["GET"])
def get_pollution_prediction():
    try:
        # Fetch real historical pollution data from the database
        historical_data = Pollution.query.order_by(Pollution.id).all()

        # Ensure there is enough data for prediction
        if not historical_data or len(historical_data) < 3:
            return jsonify({"error": "Not enough data for prediction"}), 400

        prediction_result = predict_air_quality(historical_data)
        return jsonify(prediction_result)

    except Exception as e:
        return jsonify({"error": f"Failed to predict air quality: {str(e)}"}), 500
