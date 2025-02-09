from flask import Blueprint, request, jsonify
from flask_cors import CORS
from app.models.database import db, Metering

# Importing prediction function
from app.routes.predictions.metering_prediction import predict_metering_usage

metering_bp = Blueprint('metering', __name__, url_prefix='/api/metering')
CORS(metering_bp)

# Get all metering data
@metering_bp.route('/', methods=['GET'])
def get_metering_data():
    data = Metering.query.all()
    return jsonify([{
        "id": m.id, 
        "location": m.location, 
        "water_usage": m.water_usage, 
        "energy_usage": m.energy_usage
    } for m in data])

# Get metering data by ID
@metering_bp.route('/<int:metering_id>', methods=['GET'])
def get_metering_by_id(metering_id):
    metering = Metering.query.get(metering_id)
    if not metering:
        return jsonify({"error": "Metering record not found"}), 404
    return jsonify({
        "id": metering.id, 
        "location": metering.location, 
        "water_usage": metering.water_usage, 
        "energy_usage": metering.energy_usage
    })

# Add new metering data
@metering_bp.route('/', methods=['POST'])
def add_metering():
    data = request.json
    if not data or 'location' not in data or 'water_usage' not in data or 'energy_usage' not in data:
        return jsonify({"error": "Missing data"}), 400

    new_metering = Metering(
        location=data['location'], 
        water_usage=data['water_usage'], 
        energy_usage=data['energy_usage']
    )
    db.session.add(new_metering)
    db.session.commit()
    return jsonify({"message": "Metering data added"}), 201

# Update existing metering data
@metering_bp.route('/<int:metering_id>', methods=['PUT'])
def update_metering(metering_id):
    metering = Metering.query.get(metering_id)
    if not metering:
        return jsonify({"error": "Metering record not found"}), 404

    data = request.json
    metering.location = data.get('location', metering.location)
    metering.water_usage = data.get('water_usage', metering.water_usage)
    metering.energy_usage = data.get('energy_usage', metering.energy_usage)

    db.session.commit()
    return jsonify({"message": "Metering data updated"}), 200

# Delete metering data
@metering_bp.route('/<int:metering_id>', methods=['DELETE'])
def delete_metering(metering_id):
    metering = Metering.query.get(metering_id)
    if not metering:
        return jsonify({"error": "Metering record not found"}), 404

    db.session.delete(metering)
    db.session.commit()
    return jsonify({"message": "Metering data deleted"}), 200

# Predict future metering usage
@metering_bp.route('/predict', methods=['GET'])
def predict_metering():
    try:
        # Fetch historical data for prediction
        historical_data = Metering.query.order_by(Metering.id).all()
        if len(historical_data) < 3:
            return jsonify({"error": "At least 3 data points required for prediction"}), 400

        # Call prediction function
        prediction = predict_metering_usage(historical_data)
        return jsonify(prediction), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
