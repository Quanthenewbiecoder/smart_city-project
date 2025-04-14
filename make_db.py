import sys
import os

# Add the parent directory (smart_city-project) to sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from app import create_app
from app.models.database import db

app = create_app()

with app.app_context():
    db.create_all()
    print("Database created successfully!")
