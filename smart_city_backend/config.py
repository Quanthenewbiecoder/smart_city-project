import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'your_secret_key'  # Replace with a strong secret key
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir, "smart_city.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
