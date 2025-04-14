from flask import Blueprint, render_template

frontend_bp = Blueprint('frontend', __name__)

@frontend_bp.route('/')
def dashboard():
    return render_template('dashboard.html')

@frontend_bp.route('/home')
def home():
    return render_template('home.html')
