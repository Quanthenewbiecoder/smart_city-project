from flask import Blueprint, request, jsonify
from flask_cors import CORS
from app.models.database import db, Pollution

pollution_bp = Blueprint('pollution', __name__, url_prefix='/api')
CORS(pollution_bp)

@pollution_bp.route('/', methods=['GET'])
def get_pollution_data():
    data = Pollution.query.all()
    return jsonify([{
        "id": p.id, 
        "location": p.location, 
        "air_quality_index": p.air_quality_index
    } for p in data])

@pollution_bp.route('/', methods=['POST'])
def update_pollution():
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
        
        return jsonify({"message": "Pollution data added"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
