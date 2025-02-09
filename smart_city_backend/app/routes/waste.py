from flask import Blueprint, request, jsonify
from flask_cors import CORS
from app.models.database import db, Waste

waste_bp = Blueprint('waste', __name__)
CORS(waste_bp)

@waste_bp.route('/', methods=['GET'])
def get_waste_data():
    data = Waste.query.all()
    return jsonify([{"id": w.id, "location": w.location, "bin_fill_level": w.bin_fill_level} for w in data])

@waste_bp.route('/<int:waste_id>', methods=['GET'])
def get_waste_by_id(waste_id):
    waste = Waste.query.get(waste_id)
    if not waste:
        return jsonify({"error": "Waste record not found"}), 404
    return jsonify({"id": waste.id, "location": waste.location, "bin_fill_level": waste.bin_fill_level})

@waste_bp.route('/', methods=['POST'])
def add_waste():
    data = request.json
    if not data or 'location' not in data or 'bin_fill_level' not in data:
        return jsonify({"error": "Missing data"}), 400

    new_waste = Waste(location=data['location'], bin_fill_level=data['bin_fill_level'])
    db.session.add(new_waste)
    db.session.commit()
    return jsonify({"message": "Waste data added"}), 201

@waste_bp.route('/<int:waste_id>', methods=['PUT'])
def update_waste(waste_id):
    waste = Waste.query.get(waste_id)
    if not waste:
        return jsonify({"error": "Waste record not found"}), 404

    data = request.json
    waste.location = data.get('location', waste.location)
    waste.bin_fill_level = data.get('bin_fill_level', waste.bin_fill_level)

    db.session.commit()
    return jsonify({"message": "Waste data updated"}), 200

@waste_bp.route('/<int:waste_id>', methods=['DELETE'])
def delete_waste(waste_id):
    waste = Waste.query.get(waste_id)
    if not waste:
        return jsonify({"error": "Waste record not found"}), 404

    db.session.delete(waste)
    db.session.commit()
    return jsonify({"message": "Waste data deleted"}), 200
