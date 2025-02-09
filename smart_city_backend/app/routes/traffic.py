from flask import Blueprint, request, jsonify
from flask_cors import CORS
from app.models.database import db, Traffic

# Import the prediction function
from app.routes.predictions.traffic_prediction import predict_traffic

traffic_bp = Blueprint('traffic', __name__, url_prefix='/api/traffic')
CORS(traffic_bp)

# Get all traffic data
@traffic_bp.route('/', methods=['GET'])
def get_traffic_data():
    try:
        data = Traffic.query.all()
        return jsonify([{
            "id": t.id, 
            "location": t.location, 
            "congestion_level": t.congestion_level
        } for t in data])
    except Exception as e:
        return jsonify({"error": f"Failed to fetch traffic data: {str(e)}"}), 500

# Add new traffic data
@traffic_bp.route('/', methods=['POST'])
def add_traffic():
    try:
        data = request.json
        if not data or 'location' not in data or 'congestion_level' not in data:
            return jsonify({"error": "Missing required fields: 'location' and 'congestion_level'"}), 400
        
        new_traffic = Traffic(
            location=data['location'], 
            congestion_level=data['congestion_level']
        )
        db.session.add(new_traffic)
        db.session.commit()
        return jsonify({"message": "Traffic data added successfully"}), 201
    except Exception as e:
        return jsonify({"error": f"Failed to add traffic data: {str(e)}"}), 500

# Update traffic data by ID
@traffic_bp.route('/<int:traffic_id>', methods=['PUT'])
def update_traffic(traffic_id):
    try:
        traffic = Traffic.query.get(traffic_id)
        if not traffic:
            return jsonify({"error": "Traffic record not found"}), 404

        data = request.json
        traffic.location = data.get('location', traffic.location)
        traffic.congestion_level = data.get('congestion_level', traffic.congestion_level)

        db.session.commit()
        return jsonify({"message": "Traffic data updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to update traffic data: {str(e)}"}), 500

# Delete traffic data by ID
@traffic_bp.route('/<int:traffic_id>', methods=['DELETE'])
def delete_traffic(traffic_id):
    try:
        traffic = Traffic.query.get(traffic_id)
        if not traffic:
            return jsonify({"error": "Traffic record not found"}), 404
        
        db.session.delete(traffic)
        db.session.commit()
        return jsonify({"message": "Traffic data deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to delete traffic data: {str(e)}"}), 500

# Predict future traffic congestion
@traffic_bp.route('/predict', methods=['GET'])
def predict_traffic_congestion():
    try:
        # Fetch historical traffic data
        historical_data = Traffic.query.order_by(Traffic.id).all()
        if not historical_data or len(historical_data) < 3:
            return jsonify({"error": "Not enough data for prediction"}), 400

        # Call the prediction function
        prediction_result = predict_traffic(historical_data)
        return jsonify(prediction_result), 200

    except Exception as e:
        return jsonify({"error": f"Failed to predict traffic congestion: {str(e)}"}), 500
