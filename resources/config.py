import os
from dotenv import load_dotenv


class Config:

    # Load environment variables
    load_dotenv()

    # Database connection configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('server')
    SERVER = os.environ.get('server')
    USERNAME = os.environ.get('user')
    SECRET_KEY = os.environ.get('password')
    DATABASE = os.environ.get('database')

    # SQLAlchemy configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False