from flask import Blueprint, request, jsonify
from flask_cors import CORS
from app.models.database import db, Metering

metering_bp = Blueprint('metering', __name__)
CORS(metering_bp)

@metering_bp.route('/', methods=['GET'])
def get_metering_data():
    data = Metering.query.all()
    return jsonify([{"id": m.id, "location": m.location, "water_usage": m.water_usage, "energy_usage": m.energy_usage} for m in data])

@metering_bp.route('/<int:metering_id>', methods=['GET'])
def get_metering_by_id(metering_id):
    metering = Metering.query.get(metering_id)
    if not metering:
        return jsonify({"error": "Metering record not found"}), 404
    return jsonify({"id": metering.id, "location": metering.location, "water_usage": metering.water_usage, "energy_usage": metering.energy_usage})

@metering_bp.route('/', methods=['POST'])
def add_metering():
    data = request.json
    if not data or 'location' not in data or 'water_usage' not in data or 'energy_usage' not in data:
        return jsonify({"error": "Missing data"}), 400

    new_metering = Metering(location=data['location'], water_usage=data['water_usage'], energy_usage=data['energy_usage'])
    db.session.add(new_metering)
    db.session.commit()
    return jsonify({"message": "Metering data added"}), 201

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

@metering_bp.route('/<int:metering_id>', methods=['DELETE'])
def delete_metering(metering_id):
    metering = Metering.query.get(metering_id)
    if not metering:
        return jsonify({"error": "Metering record not found"}), 404

    db.session.delete(metering)
    db.session.commit()
    return jsonify({"message": "Metering data deleted"}), 200
