import random
from flask import Blueprint, jsonify
from flask_cors import CORS
from app.models.database import db, Location, Traffic
from app.routes.predictions.traffic_prediction import predict_traffic

traffic_bp = Blueprint('traffic', __name__, url_prefix='/api/traffic')
CORS(traffic_bp)

def generate_random_traffic_data():
    """ Auto-generates random traffic data only if locations exist and prevents duplicates """
    locations = Location.query.all()
    if not locations:
        print("⚠️ No locations found! Skipping traffic data generation.")
        return

    for loc in locations:
        db.session.add(Traffic(location_id=loc.id, congestion_level=random.randint(20, 90)))
    db.session.commit()
    print("✅ Traffic data added.")

@traffic_bp.route('/', methods=['GET'])
def get_traffic_data():
    data = Traffic.query.all()
    return jsonify([{
        "id": t.id,
        "location": Location.query.get(t.location_id).name,
        "congestion_level": t.congestion_level
    } for t in data])
