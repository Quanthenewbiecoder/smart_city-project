from flask import Blueprint, request, jsonify
from flask_cors import CORS
from app.models.database import db, Waste

# Import prediction function
from app.routes.predictions.waste_prediction import predict_waste

waste_bp = Blueprint('waste', __name__, url_prefix='/api/waste')
CORS(waste_bp)

# Get all waste data
@waste_bp.route('/', methods=['GET'])
def get_waste_data():
    try:
        data = Waste.query.all()
        return jsonify([{
            "id": w.id,
            "location": w.location,
            "waste_generated": w.waste_generated
        } for w in data])
    except Exception as e:
        return jsonify({"error": f"Failed to fetch waste data: {str(e)}"}), 500

# Add new waste data
@waste_bp.route('/', methods=['POST'])
def add_waste():
    try:
        data = request.json
        if not data or 'location' not in data or 'waste_generated' not in data:
            return jsonify({"error": "Missing required fields"}), 400
        
        new_waste = Waste(
            location=data['location'],
            waste_generated=data['waste_generated']
        )
        db.session.add(new_waste)
        db.session.commit()
        return jsonify({"message": "Waste data added successfully"}), 201
    except Exception as e:
        return jsonify({"error": f"Failed to add waste data: {str(e)}"}), 500

# Delete waste data by ID
@waste_bp.route('/<int:waste_id>', methods=['DELETE'])
def delete_waste(waste_id):
    try:
        waste = Waste.query.get(waste_id)
        if not waste:
            return jsonify({"error": "Waste record not found"}), 404
        
        db.session.delete(waste)
        db.session.commit()
        return jsonify({"message": "Waste data deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to delete waste data: {str(e)}"}), 500

# Predict future waste generation
@waste_bp.route('/predict', methods=['GET'])
def predict_waste_generation():
    try:
        # Fetch historical data for prediction
        historical_data = Waste.query.order_by(Waste.id).all()
        if not historical_data or len(historical_data) < 3:
            return jsonify({"error": "Not enough data for prediction"}), 400

        # Call prediction function
        prediction = predict_waste(historical_data)
        return jsonify(prediction), 200

    except Exception as e:
        return jsonify({"error": f"Failed to predict waste generation: {str(e)}"}), 500
