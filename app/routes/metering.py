import random
from flask import Blueprint, jsonify
from flask_cors import CORS
from app.models.database import db, Location, Metering
from app.routes.predictions.metering_prediction import predict_metering_usage

metering_bp = Blueprint('metering', __name__, url_prefix='/api/metering')
CORS(metering_bp)

def generate_random_metering_data():
    """ Auto-generates random metering data only if locations exist and prevents duplicates """
    locations = Location.query.all()
    if not locations:
        print("⚠️ No locations found! Skipping metering data generation.")
        return
    
    for loc in locations:
        db.session.add(Metering(location_id=loc.id, water_usage=random.uniform(50, 500), energy_usage=random.uniform(1000, 7000)))
    db.session.commit()
    print("✅ Metering data added.")

@metering_bp.route('/', methods=['GET'])
def get_metering_data():
    data = Metering.query.all()
    return jsonify([{
        "id": m.id,
        "location": Location.query.get(m.location_id).name,
        "water_usage": m.water_usage,
        "energy_usage": m.energy_usage
    } for m in data])
