import random
from flask import Blueprint, jsonify
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from app.models.database import db, Location, Traffic
from app.routes.predictions.traffic_prediction import predict_traffic

# Traffic Blueprint
traffic_bp = Blueprint('traffic', __name__, url_prefix='/api/traffic')
CORS(traffic_bp)

def generate_random_traffic_data():
    """ Auto-generates random traffic data every 5 minutes """
    locations = Location.query.all()
    if not locations:
        return
    for loc in locations:
        db.session.add(Traffic(location_id=loc.id, congestion_level=random.randint(20, 90)))
    db.session.commit()

# Background Scheduler for Auto-Generation
scheduler = BackgroundScheduler()
scheduler.add_job(func=generate_random_traffic_data, trigger="interval", minutes=5)
scheduler.start()

@traffic_bp.route('/', methods=['GET'])
def get_traffic_data():
    data = Traffic.query.all()
    return jsonify([{"id": t.id, "location": Location.query.get(t.location_id).name, "congestion_level": t.congestion_level} for t in data])
