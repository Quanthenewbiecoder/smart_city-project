from flask import Blueprint, request, jsonify
from flask_cors import CORS
from app.models.database import Traffic

traffic_bp = Blueprint('traffic', __name__)
CORS(traffic_bp)

@traffic_bp.route('/traffic', methods=['GET'])
def get_traffic_data():
    try:
        data = Traffic.query.all()
        return jsonify([{"id": t.id, "location": t.location, "congestion_level": t.congestion_level} for t in data])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@traffic_bp.route('/traffic', methods=['POST'])
def update_traffic():
    try:
        data = request.json
        if not data or 'location' not in data or 'congestion_level' not in data:
            return jsonify({"error": "Missing data"}), 400

        new_traffic = Traffic(location=data['location'], congestion_level=data['congestion_level'])
        db.session.add(new_traffic)
        db.session.commit()
        return jsonify({"message": "Traffic data added"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
