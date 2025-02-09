import random
from flask import Blueprint, jsonify
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from app.models.database import db, Location, Pollution
from app.routes.predictions.pollution_prediction import predict_air_quality

# Pollution Blueprint
pollution_bp = Blueprint('pollution', __name__, url_prefix='/api/pollution')
CORS(pollution_bp)

def generate_random_pollution_data():
    """ Auto-generates random pollution data every 5 minutes """
    locations = Location.query.all()
    if not locations:
        return
    for loc in locations:
        db.session.add(Pollution(location_id=loc.id, air_quality_index=random.randint(30, 200)))
    db.session.commit()

# Background Scheduler for Auto-Generation
scheduler = BackgroundScheduler()
scheduler.add_job(func=generate_random_pollution_data, trigger="interval", minutes=5)
scheduler.start()

@pollution_bp.route('/', methods=['GET'])
def get_pollution_data():
    data = Pollution.query.all()
    return jsonify([{"id": p.id, "location": Location.query.get(p.location_id).name, "air_quality_index": p.air_quality_index} for p in data])
