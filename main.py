import logging
from resources.adp_requests import APIConnector
import base64
from dotenv import load_dotenv
import os
from resources.database import Database
from resources.response_filter import ResponseFilter
from resources.models import UnnormalizedEmployee, UnnormalizedTimecards
from sqlalchemy.exc import ProgrammingError


def create_tables():
    db = Database()
    engine = db.create_engine()
    try:
        db.Base.metadata.create_all(bind=engine,
                                    tables=[UnnormalizedEmployee.__table__, UnnormalizedTimecards.__table__])
    except ProgrammingError as e:
        logging.error(f"An error occurred while creating tables.\nError: {str(e)}\n")
        raise


def delete_records():
    db = Database()
    session = db.create_session()
    try:
        session.query(UnnormalizedEmployee).delete()
        session.query(UnnormalizedTimecards).delete()
        session.commit()
    except Exception as e:
        session.rollback()
        logging.error(f"An error occurred while dropping tables.\nError: {str(e)}\n")
        raise
    finally:
        session.close()


def insert_data(data):
    db = Database()
    session = db.create_session()
    try:

        if type(data) == list:
            for each_data in data:
                session.add(each_data)
            session.commit()
        else:
            session.add(data)
            session.commit()

    except Exception as e:
        session.rollback()
        logging.error(f"An error occurred.\nError: {str(e)}\n")
        raise
    finally:
        session.close()


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

    # drop_tables()
    # drop_employees_table()
    create_tables()
    delete_records()

    # Get some API responses
    employees = connector.get_employees()
    employee_data_list = ResponseFilter.get_employees(employees)

    insert_data(employee_data_list)

    time_cards = connector.get_time_cards(os.environ.get('main_associate_id'), "YYYY-MM-DD")
    time_card_list = ResponseFilter.get_timecards(time_cards)

    insert_data(time_card_list)

