from flask import Blueprint

home_bp = Blueprint("home", __name__)

@home_bp.route("/")
def index():
    return "Welcome to the Smart City Dashboard!"
