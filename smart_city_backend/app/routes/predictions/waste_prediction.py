import numpy as np
from flask import Blueprint, jsonify
from sklearn.linear_model import LinearRegression
from app.models.database import db, Waste

waste_prediction_bp = Blueprint("waste_prediction", __name__)

def predict_waste(historical_data):
    # Extract historical data
    ids = np.array([data.id for data in historical_data]).reshape(-1, 1)
    bin_fill_levels = np.array([data.bin_fill_level for data in historical_data])

    # Train the model
    model = LinearRegression()
    model.fit(ids, bin_fill_levels)

    # Predict for the next 3 periods
    future_ids = np.array([[ids[-1][0] + 1], [ids[-1][0] + 2], [ids[-1][0] + 3]])
    predicted_waste = model.predict(future_ids).tolist()

    return {
        "next_periods": [
            {"period": int(future_ids[i][0]), "predicted_bin_fill_level": round(predicted_waste[i], 2)}
            for i in range(3)
        ]
    }

# Define an API endpoint
@waste_prediction_bp.route("/predict", methods=["GET"])
def get_waste_prediction():
    try:
        # Fetch real historical waste data from the database
        historical_data = Waste.query.order_by(Waste.id).all()
        
        # Ensure there is enough data for prediction
        if not historical_data or len(historical_data) < 3:
            return jsonify({"error": "Not enough data for prediction"}), 400
        
        prediction_result = predict_waste(historical_data)
        return jsonify(prediction_result)
    
    except Exception as e:
        return jsonify({"error": f"Failed to predict waste generation: {str(e)}"}), 500
