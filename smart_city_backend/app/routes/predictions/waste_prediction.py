import numpy as np
from sklearn.linear_model import LinearRegression

def predict_waste(historical_data):
    # Extract historical data
    ids = np.array([data.id for data in historical_data]).reshape(-1, 1)
    waste_generated = np.array([data.waste_generated for data in historical_data])

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
