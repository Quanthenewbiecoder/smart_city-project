from flask import Blueprint, request, jsonify
from app.models.database import db, Metering

metering_bp = Blueprint('metering', __name__)

@metering_bp.route('/metering', methods=['GET'])
def get_metering_data():
    pass
@metering_bp.route('/metering', methods=['POST'])
def update_metering():
    pass
