from flask import Blueprint, request, jsonify
from flask_cors import CORS
from app.models.database import db, Pollution

# Import prediction function
from app.routes.predictions.pollution_prediction import predict_air_quality

pollution_bp = Blueprint('pollution', __name__, url_prefix='/api/pollution')
CORS(pollution_bp)

# Get all pollution data
@pollution_bp.route('/', methods=['GET'])
def get_pollution_data():
    try:
        data = Pollution.query.all()
        return jsonify([{
            "id": p.id, 
            "location": p.location, 
            "air_quality_index": p.air_quality_index
        } for p in data])
    except Exception as e:
        return jsonify({"error": f"Failed to fetch pollution data: {str(e)}"}), 500

# Add new pollution data
@pollution_bp.route('/', methods=['POST'])
def add_pollution():
    try:
        data = request.json
        if not data or 'location' not in data or 'air_quality_index' not in data:
            return jsonify({"error": "Missing required fields"}), 400
        
        # Check for duplicate entries
        existing_pollution = Pollution.query.filter_by(location=data['location']).first()
        if existing_pollution:
            return jsonify({"error": "Data for this location already exists"}), 409
        
        new_pollution = Pollution(
            location=data['location'], 
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
