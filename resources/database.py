from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from resources.config import Config


class Database:
    """
        A class that represents a database and provides methods to create an engine and a session.
        """
    def __init__(self):
        self.engine = self.create_engine()
        self.Session = sessionmaker(bind=self.engine)

        # Based used to define the SQLAlchemy models
        self.Base = declarative_base()

    @staticmethod
    def create_engine(server=None, database=None, username=None, password=None):
        """
        Create an engine for a SQL Server database using the specified credentials.
        If no arguments are passed, the function will use the default database config defined in the Config class.

        :param server: The name of the database server to connect to.
        :param database: The name of the database to connect to.
        :param username: The username to use for authentication.
        :param password: The password to use for authentication.
        :return: A SQL engine.
        """
        if not server:
            server = Config.SERVER
        if not database:
            database = Config.DATABASE
        if not username:
            username = Config.USERNAME
        if not password:
            password = Config.SECRET_KEY

        connection_string = f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={server}; DATABASE={database}; UID={username}; PWD={password}'
        engine = create_engine('mssql+pyodbc:///?odbc_connect=' + connection_string)
        return engine

    def create_session(self):
        """
        Create a database session using the specified engine
        :return: THe database session
        """
        session = self.Session()
        return session

    @staticmethod
    def close_session(session):
        session.close()

    def create_all_tables(self):
        self.Base.metadata.create_all(self.engine)
