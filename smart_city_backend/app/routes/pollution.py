import numpy as np
from flask import Blueprint, jsonify, request
from sklearn.linear_model import LinearRegression
from flask_cors import CORS
from app.models.database import db, Pollution, Location

pollution_bp = Blueprint('pollution', __name__, url_prefix='/api/pollution')
CORS(pollution_bp)

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

# Get all pollution data
@pollution_bp.route('/', methods=['GET'])
def get_pollution_data():
    try:
        data = Pollution.query.all()
        return jsonify([{
            "id": p.id, 
            "location": Location.query.get(p.location_id).name, 
            "air_quality_index": p.air_quality_index
        } for p in data])
    except Exception as e:
        return jsonify({"error": f"Failed to fetch pollution data: {str(e)}"}), 500

# Add new pollution data
@pollution_bp.route('/', methods=['POST'])
def add_pollution():
    try:
        data = request.json
        if not data or 'location_id' not in data or 'air_quality_index' not in data:
            return jsonify({"error": "Missing required fields"}), 400
        
        # Check for duplicate entries
        existing_pollution = Pollution.query.filter_by(location_id=data['location_id']).first()
        if existing_pollution:
            return jsonify({"error": "Data for this location already exists"}), 409
        
        new_pollution = Pollution(
            location_id=data['location_id'], 
            air_quality_index=data['air_quality_index']
        )
        db.session.add(new_pollution)
        db.session.commit()
        
        return jsonify({"message": "Pollution data added successfully"}), 201
    except Exception as e:
        return jsonify({"error": f"Failed to add pollution data: {str(e)}"}), 500

# Predict future air quality
@pollution_bp.route('/predict', methods=['GET'])
def predict_pollution():
    try:
        # Fetch historical data for prediction
        historical_data = Pollution.query.order_by(Pollution.id).all()
        if not historical_data or len(historical_data) < 3:
            return jsonify({"error": "Not enough data for prediction"}), 400

        # Call prediction function
        prediction = predict_air_quality(historical_data)
        return jsonify(prediction), 200

    except Exception as e:
        return jsonify({"error": f"Failed to predict air quality: {str(e)}"}), 500
