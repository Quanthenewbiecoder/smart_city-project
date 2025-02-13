import sys
import os
import threading
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from app import create_app
from app.models.database import db, Location
from app.routes.metering import generate_random_metering_data
from app.routes.traffic import generate_random_traffic_data
from app.routes.pollution import generate_random_pollution_data
from app.routes.waste import generate_random_waste_data

app = create_app()

# Lock to ensure only one instance runs
lock = threading.Lock()

def ensure_locations_exist():
    """ Ensures location data exists before inserting random data """
    with app.app_context():
        if Location.query.count() == 0:  
            locations = ["Downtown", "City Center", "Industrial Area", "Suburbs"]
            for name in locations:
                db.session.add(Location(name=name))
            db.session.commit()
            print("✅ Locations added to the database.")

def scheduled_data_generation():
    """ Runs auto-generation inside Flask application context """
    with lock:  # Ensures only one instance runs at a time
        with app.app_context():
            print("--------------------------------------")
            print("⏳ Generating new random data...")
            
            # Check if recent data exists
            if db.session.query(Location).count() > 0:
                generate_random_metering_data()
                generate_random_traffic_data()
                generate_random_pollution_data()
                generate_random_waste_data()
                print("✅ Random data added to the database.")
                print("--------------------------------------")
            else:
                print("⚠️ Locations missing! Skipping data generation.")

# Ensure locations exist before scheduling data generation
ensure_locations_exist()

# Scheduler for auto data generation (runs once)
scheduler = BackgroundScheduler()
scheduler.add_job(scheduled_data_generation, 'interval', minutes=1, max_instances=1)  # Runs every 5 min, max 1 instance
scheduler.start()

if __name__ == "__main__":
    try:
        app.run(debug=True, use_reloader=False)  # `use_reloader=False` prevents double execution
    except KeyboardInterrupt:
        print("❌ Shutting down Flask app...")
        scheduler.shutdown()
        print("✅ Scheduler stopped.")
