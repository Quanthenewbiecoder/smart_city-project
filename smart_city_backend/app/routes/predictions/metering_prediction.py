import numpy as np
from flask import Blueprint, jsonify
from sklearn.linear_model import LinearRegression
from app.models.database import db, Metering

# Define the Blueprint
metering_prediction_bp = Blueprint("metering_prediction", __name__)

def predict_metering_usage(historical_data):
    # Extract historical data
    ids = np.array([data.id for data in historical_data]).reshape(-1, 1)
    water_usage = np.array([data.water_usage for data in historical_data])

    # Train the model
    model = LinearRegression()
    model.fit(ids, water_usage)

    # Predict for the next 3 periods
    future_ids = np.array([[ids[-1][0] + 1], [ids[-1][0] + 2], [ids[-1][0] + 3]])
    predicted_water_usage = model.predict(future_ids).tolist()

    return {
        "next_periods": [
            {"period": int(future_ids[i][0]), "predicted_water_usage": round(predicted_water_usage[i], 2)}
            for i in range(3)
        ]
    }

# Define an API endpoint
@metering_prediction_bp.route("/predict", methods=["GET"])
def get_metering_prediction():
    try:
        # Fetch real historical metering data from the database
        historical_data = Metering.query.order_by(Metering.id).all()
        
        # Ensure there is enough data for prediction
        if not historical_data or len(historical_data) < 3:
            return jsonify({"error": "Not enough data for prediction"}), 400
        
        prediction_result = predict_metering_usage(historical_data)
        return jsonify(prediction_result)
    
    except Exception as e:
        return jsonify({"error": f"Failed to predict metering usage: {str(e)}"}), 500
