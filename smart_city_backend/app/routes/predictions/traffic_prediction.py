import numpy as np
from flask import Blueprint, jsonify
from sklearn.linear_model import LinearRegression
from app.models.database import db, Traffic

traffic_prediction_bp = Blueprint("traffic_prediction", __name__)

def predict_traffic(historical_data):
    # Extract historical data
    ids = np.array([data.id for data in historical_data]).reshape(-1, 1)
    congestion_levels = np.array([data.congestion_level for data in historical_data])

    # Train the model
    model = LinearRegression()
    model.fit(ids, congestion_levels)

    # Predict for the next 3 periods
    future_ids = np.array([[ids[-1][0] + 1], [ids[-1][0] + 2], [ids[-1][0] + 3]])
    predicted_congestion = model.predict(future_ids).tolist()

    return {
        "next_periods": [
            {"period": int(future_ids[i][0]), "predicted_congestion_level": round(predicted_congestion[i], 2)}
            for i in range(3)
        ]
    }

# Define an API endpoint
@traffic_prediction_bp.route("/predict", methods=["GET"])
def get_prediction():
    # Fetch historical traffic data from the database
    historical_data = Traffic.query.order_by(Traffic.id).all()
    if not historical_data or len(historical_data) < 3:
        return jsonify({"error": "Not enough data for prediction"}), 400
    
    prediction_result = predict_traffic(historical_data)
    return jsonify(prediction_result)
