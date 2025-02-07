from flask import Blueprint, request, jsonify
from app.models.database import db, Pollution

pollution_bp = Blueprint('pollution', __name__)

@pollution_bp.route('/pollution', methods=['GET'])
def get_pollution_data():
    pass

@pollution_bp.route('/pollution', methods=['POST'])
def update_pollution():
    pass
