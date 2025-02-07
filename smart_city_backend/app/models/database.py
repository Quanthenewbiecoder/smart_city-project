from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Traffic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    congestion_level = db.Column(db.Integer, nullable=False)  # 0-100%

class Pollution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    air_quality_index = db.Column(db.Integer, nullable=False)

class Waste(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    bin_fill_level = db.Column(db.Integer, nullable=False)  # 0-100%

class Metering(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    water_usage = db.Column(db.Float, nullable=False)
    energy_usage = db.Column(db.Float, nullable=False)

# This function initializes the database
def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
 