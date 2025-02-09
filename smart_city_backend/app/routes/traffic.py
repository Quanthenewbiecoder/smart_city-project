from flask import Blueprint, request, jsonify
from flask_cors import CORS
from app.models.database import db, Traffic

traffic_bp = Blueprint('traffic', __name__, url_prefix='/api')
CORS(traffic_bp)

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
        return jsonify({"error": str(e)}), 500

@traffic_bp.route('/', methods=['POST'])
def add_traffic():
    try:
        data = request.json
        if not data or 'location' not in data or 'congestion_level' not in data:
            return jsonify({"error": "Missing required fields"}), 400
        
        new_traffic = Traffic(
            location=data['location'], 
            congestion_level=data['congestion_level']
        )
        db.session.add(new_traffic)
        db.session.commit()
        return jsonify({"message": "Traffic data added"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@traffic_bp.route('/<int:traffic_id>', methods=['DELETE'])
def delete_traffic(traffic_id):
    try:
        traffic = Traffic.query.get(traffic_id)
        if not traffic:
            return jsonify({"error": "Traffic record not found"}), 404
        
        db.session.delete(traffic)
        db.session.commit()
        return jsonify({"message": "Traffic data deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
