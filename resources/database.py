from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


def get_engine(server, database, username, password):
    connection_url = f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={server}; DATABASE={database}; UID={username}; PWD={password}'
    engine = create_engine('mssql+pyodbc:///?odbc_connect=' + connection_url)
    return engine


def get_session(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def close_session(session):
    session.close()


# create declarative base
Base = declarative_base()
