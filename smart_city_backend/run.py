import sys
import os
import time
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "app")))

from app import create_app
from app.routes.metering import generate_random_metering_data
from app.routes.traffic import generate_random_traffic_data
from app.routes.pollution import generate_random_pollution_data
from app.routes.waste import generate_random_waste_data

app = create_app()

# Scheduler for auto data generation
scheduler = BackgroundScheduler()

def scheduled_data_generation():
    """Runs auto-generation inside Flask application context"""
    with app.app_context():
        print("⏳ Generating new random data...")
        generate_random_metering_data()
        generate_random_traffic_data()
        generate_random_pollution_data()
        generate_random_waste_data()
        print("✅ Random data added to the database.")

# Run every 5 minutes
scheduler.add_job(scheduled_data_generation, 'interval', minutes=5)
scheduler.start()

if __name__ == "__main__":
    try:
        app.run(debug=True)
    except KeyboardInterrupt:
        print("❌ Shutting down Flask app...")
        scheduler.shutdown()
        print("✅ Scheduler stopped.")
