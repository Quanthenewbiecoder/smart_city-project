from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)

    # Relationship to other tables
    traffics = db.relationship("Traffic", backref="location", lazy=True)
    pollutions = db.relationship("Pollution", backref="location", lazy=True)
    wastes = db.relationship("Waste", backref="location", lazy=True)
    meterings = db.relationship("Metering", backref="location", lazy=True)

class Traffic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey("location.id"), nullable=False, index=True)
    congestion_level = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)

    def delete(self):
        self.deleted_at = datetime.utcnow()
        db.session.commit()

class Pollution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey("location.id"), nullable=False, index=True)
    air_quality_index = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)

    def delete(self):
        self.deleted_at = datetime.utcnow()
        db.session.commit()

class Waste(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey("location.id"), nullable=False, index=True)
    bin_fill_level = db.Column(db.Integer, nullable=False)  # 0-100%
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)

    def delete(self):
        self.deleted_at = datetime.utcnow()
        db.session.commit()

class Metering(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey("location.id"), nullable=False, index=True)
    water_usage = db.Column(db.Float, nullable=False)
    energy_usage = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)

    def delete(self):
        self.deleted_at = datetime.utcnow()
        db.session.commit()

# Initialize the database
def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()

        # Generate sample data dynamically
        locations = ["Downtown", "City Center", "Industrial Area", "Suburbs"]
        if not Location.query.first():
            db.session.add_all([Location(name=loc) for loc in locations])
            db.session.commit()

        # Get a sample location
        loc = Location.query.first()

        # Sample data generation logic
        def add_sample_data(model, **kwargs):
            if not model.query.first():
                sample_data = [model(location_id=loc.id, **kwargs)]
                db.session.add_all(sample_data)
                db.session.commit()

        add_sample_data(Traffic, congestion_level=50)
        add_sample_data(Traffic, congestion_level=70)
        
        add_sample_data(Pollution, air_quality_index=65)
        add_sample_data(Pollution, air_quality_index=80)
        
        add_sample_data(Waste, bin_fill_level=30)
        add_sample_data(Waste, bin_fill_level=75)

        add_sample_data(Metering, water_usage=500.5, energy_usage=1200.8)
        add_sample_data(Metering, water_usage=600.0, energy_usage=1500.2)
