import random
from flask import Blueprint, jsonify
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from app.models.database import db, Location, Waste
from app.routes.predictions.waste_prediction import predict_waste

# Waste Blueprint
waste_bp = Blueprint('waste', __name__, url_prefix='/api/waste')
CORS(waste_bp)

def generate_random_waste_data():
    """ Auto-generates random waste data every 5 minutes """
    locations = Location.query.all()
    if not locations:
        return
    for loc in locations:
        db.session.add(Waste(location_id=loc.id, bin_fill_level=random.randint(10, 100)))
    db.session.commit()

# Background Scheduler for Auto-Generation
scheduler = BackgroundScheduler()
scheduler.add_job(func=generate_random_waste_data, trigger="interval", minutes=5)
scheduler.start()

@waste_bp.route('/', methods=['GET'])
def get_waste_data():
    data = Waste.query.all()
    return jsonify([{"id": w.id, "location": Location.query.get(w.location_id).name, "bin_fill_level": w.bin_fill_level} for w in data])
