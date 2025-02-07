from flask import Blueprint, request, jsonify
from app.models.database import db, Waste

waste_bp = Blueprint('waste', __name__)

@waste_bp.route('/waste', methods=['GET'])
def get_waste_data():
    pass

@waste_bp.route('/waste', methods=['POST'])
def update_waste():
    pass