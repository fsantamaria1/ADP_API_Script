from resources.adp_requests import APIConnector
import base64
from resources.database import get_engine, get_session, Base
from dotenv import load_dotenv
import os


def create_tables():
    engine = get_engine('server', 'database', 'username', 'password')
    Base.metadata.create_all(engine)


def insert_data():
    engine = get_engine('server', 'database', 'username', 'password')
    session = get_session(engine)
    session.commit()
    session.close()


# TODO: Work on the create_table and insert_data functions

if __name__ == '__main__':
    # Load environment variables
    load_dotenv()

    # Encode credentials and convert to base 64
    client_id_secret = f"{os.environ.get('client_id')}:{os.environ.get('client_secret')}"
    byte_credentials = client_id_secret.encode('ascii')
    base64_byte_credentials = base64.b64encode(byte_credentials)
    base64_credentials = base64_byte_credentials.decode('ascii')

    # Create APIConnector class object to get all the necessary responses
    certificate = (os.environ.get('cert_file_path'), os.environ.get('key_file_path'))
    connector = APIConnector(certificate, base64_credentials)

    # Get some API responses
    employees = connector.get_employees("number_of_employees")

    time_cards = connector.get_time_cards("number_of_time_cards", os.environ.get('main_associate_id'), "YYYY-MM-DD")
