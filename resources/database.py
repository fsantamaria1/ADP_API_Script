import pyodbc


class SQLConnector:
    def __init__(self, server: str, database: str, username: str, password: str):
        """
                Initialize an instance of the MsSqlDatabase class.

                Args:
                    server (str): The name or IP address of the SQL Server.
                    database (str): The name of the database.
                    username (str): The username used to connect to the database.
                    password (str): The password used to connect to the database.
                """
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.connection = None
        self.cursor = None

    def connect(self):
        """
                Establish a connection to the database.

                Returns:
                    pyodbc.Connection: A pyodbc Connection object representing the database connection.
                """
        self.connection = pyodbc.connect(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password}"
        )
        self.cursor = self.connection.cursor()

    def insert_data(self, table_name, data):
        """
                Insert multiple records into the specified table.

                Args:
                    table_name (str): The name of the table to insert the records into.
                    data (list): A list of dictionaries, where each dictionary represents a record to be inserted.
                """
        # TODO: Write code to insert data into the specified table

    def disconnect(self):
        """
            Disconnect cursor and connection to database.
        """
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
