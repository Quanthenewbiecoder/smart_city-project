from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)  # Index for faster lookups

class Traffic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False, index=True)  # Indexed for speed
    congestion_level = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)  # Index for sorting
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)  # Soft delete

    def delete(self):
        self.deleted_at = datetime.utcnow()
        db.session.commit()

class Pollution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    air_quality_index = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)  # Soft delete

    def delete(self):
        self.deleted_at = datetime.utcnow()
        db.session.commit()

class Waste(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    bin_fill_level = db.Column(db.Integer, nullable=False)  # 0-100%
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)  # Soft delete

    def delete(self):
        self.deleted_at = datetime.utcnow()
        db.session.commit()

class Metering(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    water_usage = db.Column(db.Float, nullable=False)
    energy_usage = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)  # Soft delete

    def delete(self):
        self.deleted_at = datetime.utcnow()
        db.session.commit()

# This function initializes the database
def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()

        # Add locations if none exist
        if not Location.query.first():
            locations = ["Downtown", "City Center", "Industrial Area", "Suburbs"]
            db.session.add_all([Location(name=loc) for loc in locations])
            db.session.commit()

        # Get a sample location
        loc = Location.query.first()

        # Add Traffic sample data
        if not Traffic.query.first():
            sample_traffic = [
                Traffic(location_id=loc.id, congestion_level=50),
                Traffic(location_id=loc.id, congestion_level=70)
            ]
            db.session.add_all(sample_traffic)
            db.session.commit()

        # Add Pollution sample data
        if not Pollution.query.first():
            sample_pollution = [
                Pollution(location_id=loc.id, air_quality_index=65),
                Pollution(location_id=loc.id, air_quality_index=80)
            ]
            db.session.add_all(sample_pollution)
            db.session.commit()

        # Add Waste sample data
        if not Waste.query.first():
            sample_waste = [
                Waste(location_id=loc.id, bin_fill_level=30),
                Waste(location_id=loc.id, bin_fill_level=75)
            ]
            db.session.add_all(sample_waste)
            db.session.commit()

        # Add Metering sample data
        if not Metering.query.first():
            sample_metering = [
                Metering(location_id=loc.id, water_usage=500.5, energy_usage=1200.8),
                Metering(location_id=loc.id, water_usage=600.0, energy_usage=1500.2)
            ]
            db.session.add_all(sample_metering)
            db.session.commit()



 