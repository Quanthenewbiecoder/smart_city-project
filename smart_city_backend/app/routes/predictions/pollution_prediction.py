import numpy as np
from flask import Blueprint, jsonify
from sklearn.linear_model import LinearRegression

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
    # Dummy historical data for testing (replace with actual database query)
    class DummyData:
        def __init__(self, _id, air_quality_index):
            self.id = _id
            self.air_quality_index = air_quality_index

    historical_data = [DummyData(i, np.random.randint(50, 150)) for i in range(1, 11)]
    prediction_result = predict_air_quality(historical_data)

    return jsonify(prediction_result)
