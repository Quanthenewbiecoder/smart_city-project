from flask import Blueprint, jsonify
from app.routes.dashboard import get_real_data
from app.routes.predictions.traffic_prediction import predict_traffic
from app.routes.predictions.pollution_prediction import predict_air_quality
from app.routes.predictions.waste_prediction import predict_waste
from app.routes.predictions.metering_prediction import predict_metering_usage
from app.models.database import Traffic, Pollution, Waste, Metering

home_bp = Blueprint("home", __name__, url_prefix="/api/home")

@home_bp.route("/")
def index():
    return jsonify({"message": "Welcome to the Smart City Dashboard!"})

@home_bp.route("/data", methods=["GET"])
def get_all_data():
    """Fetches real-time dashboard data and predictions."""
    try:
        # Fetch real-time data
        real_data = get_real_data()

        # Fetch historical data for predictions
        traffic_data = Traffic.query.order_by(Traffic.id).all()
        pollution_data = Pollution.query.order_by(Pollution.id).all()
        waste_data = Waste.query.order_by(Waste.id).all()
        metering_data = Metering.query.order_by(Metering.id).all()

        # Generate predictions if enough data exists
        predictions = {
            "traffic": predict_traffic(traffic_data) if len(traffic_data) >= 3 else {"error": "Not enough data for traffic prediction"},
            "pollution": predict_air_quality(pollution_data) if len(pollution_data) >= 3 else {"error": "Not enough data for pollution prediction"},
            "waste": predict_waste(waste_data) if len(waste_data) >= 3 else {"error": "Not enough data for waste prediction"},
            "metering": predict_metering_usage(metering_data) if len(metering_data) >= 3 else {"error": "Not enough data for metering prediction"}
        }

        # Construct and return JSON response
        response = {
            "dashboard": real_data,
            "predictions": predictions
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": f"Failed to retrieve data: {str(e)}"}), 500
