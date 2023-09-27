import os
from os.path import join, dirname
from dotenv import load_dotenv


class Config:
    """
    Contains credentials and information used to connect to the MS SQL server
    """
    # Load environment variables
    dotenv_path = join(dirname(__file__), '../.env')
    load_dotenv(dotenv_path)
    # load_dotenv()

    # Database connection configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('server')
    SERVER = os.environ.get('server')
    USERNAME = os.environ.get('user')
    SECRET_KEY = os.environ.get('password')
    DATABASE = os.environ.get('database')

    # SQLAlchemy configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False
