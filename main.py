from resources.adp_requests import APIConnector
import base64
import time


# Get a list of employees from ADP API
def get_list_of_employees(total_number):
    employees_list = connector.get_employees(total_number)
    return employees_list


# Get a list of time cards for a specific associate from ADP API
def get_list_of_time_cards(total_number, main_associate_oid, start_date):
    time_card_list = connector.get_time_cards(total_number, main_associate_oid, start_date)
    return time_card_list


# Start time to measure performance
start_time = time.time()
print(start_time)

# ADP API credentials
client_id = "client_id"
client_secret = "client_secret"
client_id_secret = f"{client_id}:{client_secret}"

# Main Associate_ID
main_associate_id = "AOID"

# Encode credentials and convert to base 64
byte_credentials = client_id_secret.encode('ascii')
base64_byte_credentials = base64.b64encode(byte_credentials)
base64_credentials = base64_byte_credentials.decode('ascii')

# URL used to get the bearer token
url = "https://accounts.adp.com/auth/oauth/v2/token?grant_type=client_credentials"

# Paths to the PEM and KEY files
cert_file_path = r"path"
key_file_path = r"path"
certificate = (cert_file_path, key_file_path)

# Create an instance of ApiConnector class
connector = APIConnector(certificate, str(base64_credentials))

# Get a list of employees
employees = get_list_of_employees(500)

# Get a list of time cards
time_cards = get_list_of_time_cards(500, main_associate_id, "YYYY-MM-DD")

