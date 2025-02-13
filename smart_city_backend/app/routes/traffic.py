import random
from flask import Blueprint, jsonify
from flask_cors import CORS
from app.models.database import db, Location, Waste
from app.routes.predictions.waste_prediction import predict_waste

waste_bp = Blueprint('waste', __name__, url_prefix='/api/waste')
CORS(waste_bp)

def generate_random_waste_data():
    """ Auto-generates random waste data only if locations exist and prevents duplicates """
    locations = Location.query.all()
    if not locations:
        print("⚠️ No locations found! Skipping waste data generation.")
        return
    
    for loc in locations:
        db.session.add(Waste(location_id=loc.id, bin_fill_level=random.randint(10, 100)))
    db.session.commit()
    print("✅ Waste data added.")

@waste_bp.route('/', methods=['GET'])
def get_waste_data():
    data = Waste.query.all()
    return jsonify([{
        "id": w.id,
        "location": Location.query.get(w.location_id).name,
        "bin_fill_level": w.bin_fill_level
    } for w in data])
