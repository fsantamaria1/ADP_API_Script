import requests
import json
import logging
import time


class URLGenerator:
    """
    Helper class for generating URLs for ADP API calls.
    """

    def __init__(self):

        # Endpoints for API calls
        self.timecard_api_endpoint = "https://api.adp.com/time/v2/workers"
        self.employee_api_endpoint = "https://api.adp.com/hr/v2/workers"

    @staticmethod
    def generate_api_url(api_endpoint: str, top: int, skip: int, args=None):
        """
         Generates an API URL with the specified parameters.
        :param api_endpoint: The base URL for the API.
        :param top: The number of records to retrieve.
        :param skip: The number of records to skip.
        :param args: Additional parameters for the API call.
        :return: The complete URL for the API call.
        """

        if args is not None:
            return f"{api_endpoint}/{args}$top={top}&$skip={skip}"
        else:
            return f"{api_endpoint}?$top={top}&$skip={skip}"

    def generate_employee_api_urls_(self, max_number_of_records: int):
        """
        Generates a list of URLs for retrieving employee data.
        :param max_number_of_records: The maximum number of records to retrieve.
        :return: A list of URLs for retrieving employee data.
        """

        processed = 0
        top = 50
        skip = 0
        list_of_employee_urls = []
        while processed <= max_number_of_records:
            employee_url = self.generate_api_url(self.employee_api_endpoint, top, skip)
            list_of_employee_urls.append(employee_url)
            skip += 50
            processed += 50
        return list_of_employee_urls

    def generate_timecard_api_urls(self, max_number_of_records: int, start_date, main_associate_id: str):
        """
        Generates a list of URLs for retrieving timecard data.
        :param max_number_of_records: The maximum number of records to retrieve.
        :param start_date: The start date for the timecard data.
        :param main_associate_id: The ID of the associate id used to retrieve all the team time cards.
        :return: A list of URLs for retrieving timecard data.
        """

        processed = 0
        top = 25
        skip = 0
        list_of_time_card_urls = []
        rest_of_url = f"{main_associate_id}/team-time-cards?$expand=dayEntries&"
        while processed <= max_number_of_records:
            time_card_url = self.generate_api_url(self.timecard_api_endpoint, top, skip, rest_of_url)
            time_card_url = f"{time_card_url}&$filter=timeCards/timePeriod/startDate eq '{start_date}'"
            list_of_time_card_urls.append(time_card_url)
            skip += 25
            processed += 25
        return list_of_time_card_urls


class APIConnector:
    """
    Class for connecting to the ADP API and retrieving data.
    """

    def __init__(self, full_certificate: tuple[str, str], base_64_credentials: str):
        """
        Initializes the class with the provided certificate.
        :param full_certificate: The certificate to use for the API requests.
        :param base_64_credentials: The base64 encoded client id and secret for authentication.
        """

        self.certificate = full_certificate
        self.payload = {}
        self.files = {}
        self.token = None
        self.token_expiration = None
        self.base64_credentials = base_64_credentials
        self.token_api_endpoint = "https://accounts.adp.com/auth/oauth/v2/token?grant_type=client_credentials"
        self.api_host = "api.adp.com"
        self.url_generator = URLGenerator()

    def get_token(self):
        """
        Retrieves a bearer token from the ADP API and returns it.
        Raises: requests.exceptions.RequestException: If an error occurs while making the request.

        """

        try:
            headers = {
                'Authorization': f'Basic {self.base64_credentials}'
            }
            response = requests.request("POST",
                                        url=self.token_api_endpoint,
                                        headers=headers,
                                        data=self.payload,
                                        files=self.files,
                                        cert=self.certificate)

            # Parse the response to get the token
            bearer_token_response = json.loads(response.text)
            access_token = bearer_token_response.get('access_token')
            bearer_token = f"Bearer {access_token}"
            # Set the token and the expiration time (60 minutes)
            self.token = bearer_token
            self.token_expiration = time.time() + 3600

        except requests.exceptions.RequestException as e:
            logging.error(f"An error occurred while retrieving the token from {self.token_api_endpoint}: {e}")
            raise

    def verify_token(self):
        """
            Verifies whether the token is active or not and generates a new token if it is not currently active
        """
        if self.token is None or self.token_expiration is None or time.time() > self.token_expiration:
            try:
                self.get_token()
            except Exception as e:
                logging.error(f"An error occurred while verifying token: {str(e)}")

    def get_time_cards(self, max_number_of_time_cards, main_associate_id, start_date):
        """
        Retrieves a list of time cards from the ADP API.

        :param max_number_of_time_cards: The maximum number of time cards to retrieve.
        :param main_associate_id: The associate ID of the main employee to retrieve their team time cards.
        :param start_date: The pay period start date. It is always a Monday's date and in this format: YYYY_MM-DD
        :return: A list of JSONs which contain time card information
        """
        self.verify_token()
        list_of_urls = self.url_generator.generate_timecard_api_urls(max_number_of_time_cards,
                                                                     start_date,
                                                                     main_associate_id)
        try:
            list_of_time_cards = []
            headers = {
                'Authorization': self.token,
                'Accept-Encoding': 'gzip, deflate',
                'Host': self.api_host,
                'Connection': 'Keep-Alive',
                'User-Agent': 'Apache-HttpClient/4.5.2(Java/1.8.0_112)',
                'Accept': 'application/json',
                'Cookie': 'BIGipServerp_dc1_mobile_sor_integratedezlm=3938124043.15395.0000; BIGipServerp_dc2_mobile_apache_sor=3013608203.5377.0000; BIGipServerp_mkplproxy-dc1=1633878283.20480.0000; BIGipServerp_mkplproxy-dc2=670892811.20480.0000; BIGipServerp_dc1_mobile_apache_sor=153042955.5377.0000; Cookie_1=value'
            }
            for time_card_url in list_of_urls:
                with requests.request(
                        "GET",
                        url=time_card_url,
                        headers=headers,
                        data=self.payload,
                        cert=self.certificate
                ) as response:

                    if response.status_code == 200:
                        response_text = json.loads(response.text)
                        complete_indicator = response_text.get("meta").get("completeIndicator")

                        if complete_indicator:
                            return list_of_time_cards

                        list_of_time_cards.append(response_text)

                    else:
                        response.raise_for_status()

        except Exception as e:
            logging.error(f"An error occurred while retrieving time cards.\n Error: {str(e)}\n")
            raise

    def get_employees(self, max_number_of_employees):
        """
        Retrieves a list of employees from the ADP API.
        :param max_number_of_employees: The maximum number of employees to retrieve.
        :return: A list of employees in JSON format.
        """

        self.verify_token()

        try:
            list_of_urls = self.url_generator.generate_employee_api_urls_(max_number_of_employees)
            list_of_employees = []
            headers = {
                'Authorization': self.token,
                'Cookie': 'BIGipServerp_dc1_mobile_apache_sor=706691083.5377.0000; BIGipServerp_mkplproxy-dc1=2803368203.20480.0000; BIGipServerp_mkplproxy-dc2=654115595.20480.0000'
            }
            for employee_url in list_of_urls:
                with requests.request(
                        "GET",
                        url=employee_url,
                        headers=headers,
                        data=self.payload,
                        cert=self.certificate
                ) as response:

                    if response.status_code == 200:
                        response_text = json.loads(response.text)
                        list_of_employees.append(response_text)

                    elif response.status_code == 204:
                        break

                    else:
                        response.raise_for_status()

            return list_of_employees

        except Exception as e:
            logging.error(
                f"An error occurred while retrieving employees.\n Error: {str(e)}\n")
            raise
