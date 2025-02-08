from flask import Blueprint, request, jsonify
from flask_cors import CORS
from app.models.database import db, Waste

waste_bp = Blueprint('waste', __name__)
CORS(waste_bp)

@waste_bp.route('/waste', methods=['GET'])
def get_waste_data():
    data = Waste.query.all()
    return jsonify([{"id": w.id, "location": w.location, "bin_fill_level": w.bin_fill_level} for w in data])

@waste_bp.route('/waste', methods=['POST'])
def update_waste():
    data = request.json
    new_waste = Waste(location=data['location'], bin_fill_level=data['bin_fill_level'])
    db.session.add(new_waste)
    db.session.commit()
    return jsonify({"message": "Waste data added"}), 201
