import numpy as np
from flask import Blueprint, jsonify
from sklearn.linear_model import LinearRegression

waste_prediction_bp = Blueprint("waste_prediction", __name__)

def predict_waste(historical_data):
    # Extract historical data
    ids = np.array([data.id for data in historical_data]).reshape(-1, 1)
    waste_generated = np.array([data.bin_fill_level for data in historical_data])

    # Train the model
    model = LinearRegression()
    model.fit(ids, waste_generated)

    # Predict for the next 3 periods
    future_ids = np.array([[ids[-1][0] + 1], [ids[-1][0] + 2], [ids[-1][0] + 3]])
    predicted_waste = model.predict(future_ids).tolist()

    return {
        "next_periods": [
            {"period": int(future_ids[i][0]), "predicted_waste_generated": round(predicted_waste[i], 2)}
            for i in range(3)
        ]
    }

# Define an API endpoint
@waste_prediction_bp.route("/predict", methods=["GET"])
def get_waste_prediction():
    # Dummy historical data for testing (replace with actual database query)
    class DummyData:
        def __init__(self, _id, waste_generated):
            self.id = _id
            self.waste_generated = waste_generated

    historical_data = [DummyData(i, np.random.randint(100, 500)) for i in range(1, 11)]
    prediction_result = predict_waste(historical_data)

    return jsonify(prediction_result)
