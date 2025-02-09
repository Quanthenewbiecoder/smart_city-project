import numpy as np
from sklearn.linear_model import LinearRegression

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
