from flask import Blueprint, jsonify
from app.routes.predictions.traffic_prediction import predict_traffic
from app.routes.predictions.pollution_prediction import predict_air_quality
from app.routes.predictions.waste_prediction import predict_waste
from app.routes.predictions.metering_prediction import predict_metering_usage
from app.models.database import db, Traffic, Pollution, Waste, Metering, Location

home_bp = Blueprint("home", __name__, url_prefix="/api/home")

@home_bp.route("/")
def index():
    return jsonify({"message": "Welcome to the Smart City Dashboard!"})

def get_latest_generated_data():
    """ Fetches the most recent generated data for each category. """
    
    def get_location_name(location_id):
        location = Location.query.get(location_id)
        return location.name if location else "Unknown Location"

    latest_traffic = Traffic.query.order_by(Traffic.id.desc()).limit(1).all()
    latest_pollution = Pollution.query.order_by(Pollution.id.desc()).limit(1).all()
    latest_waste = Waste.query.order_by(Waste.id.desc()).limit(1).all()
    latest_metering = Metering.query.order_by(Metering.id.desc()).limit(1).all()

    return {
        "traffic": [{"location": get_location_name(t.location_id), "congestion_level": t.congestion_level} for t in latest_traffic],
        "pollution": [{"location": get_location_name(p.location_id), "air_quality_index": p.air_quality_index} for p in latest_pollution],
        "waste": [{"location": get_location_name(w.location_id), "bin_fill_level": w.bin_fill_level} for w in latest_waste],
        "metering": [{"location": get_location_name(m.location_id), "water_usage": m.water_usage, "energy_usage": m.energy_usage} for m in latest_metering]
    }

@home_bp.route("/data", methods=["GET"])
def get_home_data():
    """ Retrieves only the most recent generated data and its predictions. """
    latest_data = get_latest_generated_data()

    # Fetch the latest 3 records for predictions
    latest_traffic_data = Traffic.query.order_by(Traffic.id.desc()).limit(3).all()
    latest_pollution_data = Pollution.query.order_by(Pollution.id.desc()).limit(3).all()
    latest_waste_data = Waste.query.order_by(Waste.id.desc()).limit(3).all()
    latest_metering_data = Metering.query.order_by(Metering.id.desc()).limit(3).all()

    # Generate predictions based on the last 3 generated records
    traffic_prediction = predict_traffic(latest_traffic_data) if len(latest_traffic_data) >= 3 else {"error": "Not enough data for traffic prediction"}
    pollution_prediction = predict_air_quality(latest_pollution_data) if len(latest_pollution_data) >= 3 else {"error": "Not enough data for pollution prediction"}
    waste_prediction = predict_waste(latest_waste_data) if len(latest_waste_data) >= 3 else {"error": "Not enough data for waste prediction"}
    metering_prediction = predict_metering_usage(latest_metering_data) if len(latest_metering_data) >= 3 else {"error": "Not enough data for metering prediction"}

    return jsonify({
        "latest_data": latest_data,
        "predictions": {
            "traffic": traffic_prediction,
            "pollution": pollution_prediction,
            "waste": waste_prediction,
            "metering": metering_prediction
        }
    })
