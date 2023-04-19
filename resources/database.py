from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from resources.config import Config


def get_engine(server=None, database=None, username=None, password=None):
    """
    Create an engine for a SQL Server database using the specified credentials.
    If no arguments are passed, the function will use the default database config defined in the DATABASE_CONFIG dictionary.
    :param server: The server's IP or hostname
    :param database: The database with the required tables
    :param username: The username that will be used to initialize the session
    :param password: The password that will be used to initialize the session
    :return: The SQL engine
    """

    if not server:
        server = Config.SERVER
    if not database:
        database = Config.DATABASE
    if not username:
        username = Config.USERNAME
    if not password:
        password = Config.SECRET_KEY
        
    connection_url = f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={server}; DATABASE={database}; UID={username}; PWD={password}'
    engine = create_engine('mssql+pyodbc:///?odbc_connect=' + connection_url)
    return engine


def get_session(engine):
    """
    Create a database session using the specified engine
    :param engine: The SQL engine that will be used for the session
    :return: THe database session
    """
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def close_session(session):
    session.close()


# create declarative base
Base = declarative_base()
