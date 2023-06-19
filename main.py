from resources.adp_requests import APIConnector
import base64
from dotenv import load_dotenv
import os
from resources.response_filter import ResponseFilter
from resources.models import UnnormalizedEmployees, UnnormalizedTimecards
from resources.database_functions import *
from resources.date_util import DateUtil
import datetime
import time
import schedule


def encode_credentials(client_id, client_secret):
    """Encode client ID and client secret and return the resulting Base64 credentials."""
    client_id_secret = f"{client_id}:{client_secret}"
    byte_credentials = client_id_secret.encode('ascii')
    base64_byte_credentials = base64.b64encode(byte_credentials)
    return base64_byte_credentials.decode('ascii')


def update_dependent_tables(schema_name, procedure_names):
    """Call stored procedures to update dependent tables."""
    for procedure_name in procedure_names:
        call_stored_procedure(schema_name, procedure_name)


def get_time_cards(connector, date_list):
    """Get weekly time cards for the date(s) provided and return list of time cards"""
    if isinstance(date_list, str):
        date_list = [date_list]
    time_cards = []
    for date in date_list:
        time_cards_for_date = connector.get_time_cards(os.environ.get('main_associate_id'), date)
        time_card_list = ResponseFilter.get_timecards(time_cards_for_date)
        time_cards.extend(time_card_list)
    return time_cards


def main():
    # Load environment variables
    load_dotenv()

    # Encode client ID and client secret and convert to Base64
    base64_credentials = encode_credentials(os.environ.get('client_id'), os.environ.get('client_secret'))

    # Create APIConnector class object to get all the necessary responses
    certificate = (os.environ.get('cert_file_path'), os.environ.get('key_file_path'))
    connector = APIConnector(certificate, base64_credentials)

    # Create non-normalized tables if they don't exist
    create_tables(UnnormalizedEmployees)
    create_tables(UnnormalizedTimecards)

    # Delete any existing records in the non-normalized employees table if it already existed
    delete_records(UnnormalizedEmployees)
    delete_records(UnnormalizedTimecards)

    # Get employee information and insert it into the Unnormalized table
    employees = connector.get_employees()
    employee_data_list = ResponseFilter.get_employees(employees)
    insert_data(employee_data_list)

    # Call stored procedures to update dependent employee tables
    update_dependent_tables(os.environ.get('adp_schema'), [
        os.environ.get('emp_procedure_1'),
        os.environ.get('emp_procedure_2'),
        os.environ.get('emp_procedure_3'),
        os.environ.get('emp_procedure_4')
    ])

    # Get list of the last three mondays
    list_of_dates = DateUtil.get_mondays(3)

    # # Get time cards and insert them into the Unnormalized table
    # Can provide YYYY-MM-DD or ['YYYY-MM-DD', 'YYYY-MM-DD', ...]
    time_cards = get_time_cards(connector, list_of_dates)
    insert_data(time_cards)

    # Call stored procedures to update dependent time card tables
    update_dependent_tables(os.environ.get('adp_schema'), [
        os.environ.get('tc_procedure_1'),
        os.environ.get('tc_procedure_2'),
        os.environ.get('tc_procedure_3'),
        os.environ.get('tc_procedure_4'),
        os.environ.get('tc_procedure_5'),
        os.environ.get('tc_procedure_6')
    ])


if __name__ == '__main__':
    main()
