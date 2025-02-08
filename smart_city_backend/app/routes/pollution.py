from flask import Blueprint, request, jsonify
from flask_cors import CORS
from app.models.database import db, Pollution

pollution_bp = Blueprint('pollution', __name__)
CORS(pollution_bp)

@pollution_bp.route('/pollution', methods=['GET'])
def get_pollution_data():
    data = Pollution.query.all()
    return jsonify([{"id": p.id, "location": p.location, "air_quality_index": p.air_quality_index} for p in data])

@pollution_bp.route('/pollution', methods=['POST'])
def update_pollution():
    data = request.json
    new_pollution = Pollution(location=data['location'], air_quality_index=data['air_quality_index'])
    db.session.add(new_pollution)
    db.session.commit()
    return jsonify({"message": "Pollution data added"}), 201