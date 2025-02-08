from flask import Blueprint, request, jsonify
from flask_cors import CORS
from app.models.database import db, Metering

metering_bp = Blueprint('metering', __name__)
CORS(metering_bp)

@metering_bp.route('/metering', methods=['GET'])
def get_metering_data():
    data = Metering.query.all()
    return jsonify([{"id": m.id, "location": m.location, "water_usage": m.water_usage, "energy_usage": m.energy_usage} for m in data])

@metering_bp.route('/metering', methods=['POST'])
def update_metering():
    data = request.json
    new_metering = Metering(location=data['location'], water_usage=data['water_usage'], energy_usage=data['energy_usage'])
    db.session.add(new_metering)
    db.session.commit()
    return jsonify({"message": "Metering data added"}), 201
