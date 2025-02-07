from flask import Blueprint, request, jsonify
from app.models.database import db, Traffic

traffic_bp = Blueprint('traffic', __name__)

@traffic_bp.route('/traffic', methods=['GET'])
def get_traffic_data():
    pass

@traffic_bp.route('/traffic', methods=['POST'])
def update_traffic():
    pass
