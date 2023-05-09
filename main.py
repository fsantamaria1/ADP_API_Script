from resources.adp_requests import APIConnector
import base64
from dotenv import load_dotenv
import os
from resources.response_filter import ResponseFilter
from resources.models import UnnormalizedEmployees, UnnormalizedTimecards
from resources.database_functions import *


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

    # Create non-normalized tables
    create_tables(UnnormalizedEmployees)
    create_tables(UnnormalizedTimecards)

    # Delete any existing records in the non-normalized employees table if it already existed
    delete_records(UnnormalizedEmployees)

    # Get some API responses and insert the data into the database
    employees = connector.get_employees()
    employee_data_list = ResponseFilter.get_employees(employees)

    insert_data(employee_data_list)

    time_cards = connector.get_time_cards(os.environ.get('main_associate_id'), "YYYY-MM-DD")
    time_card_list = ResponseFilter.get_timecards(time_cards)

    insert_data(time_card_list)

    # Call stored procedures to update dependent tables
    call_stored_procedure(os.environ.get('timecard_schema'), os.environ.get('tc_procedure_1'))
    call_stored_procedure(os.environ.get('timecard_schema'), os.environ.get('tc_procedure_2'))
    call_stored_procedure(os.environ.get('timecard_schema'), os.environ.get('tc_procedure_3'))
    call_stored_procedure(os.environ.get('timecard_schema'), os.environ.get('tc_procedure_4'))
    call_stored_procedure(os.environ.get('timecard_schema'), os.environ.get('tc_procedure_5'))
    call_stored_procedure(os.environ.get('timecard_schema'), os.environ.get('tc_procedure_6'))
