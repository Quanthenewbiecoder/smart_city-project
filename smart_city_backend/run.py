import sys
import os
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from app import create_app
from app.routes.metering import generate_random_metering_data
from app.routes.traffic import generate_random_traffic_data
from app.routes.pollution import generate_random_pollution_data
from app.routes.waste import generate_random_waste_data

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "app")))

# Create Flask app
app = create_app()

# Initialize APScheduler
scheduler = BackgroundScheduler()

def scheduled_data_generation():
    print("⏳ Generating new random data...")  # Logs to console
    generate_random_metering_data()
    generate_random_traffic_data()
    generate_random_pollution_data()
    generate_random_waste_data()
    print("✅ New random data added!")

# Schedule the task every 5 minutes
scheduler.add_job(scheduled_data_generation, 'interval', minutes=5)
scheduler.start()

if __name__ == "__main__":
    print("🚀 Starting Flask with APScheduler enabled...")
    app.run(debug=True, use_reloader=False)  # Disable reloader to prevent duplicate scheduler jobs
