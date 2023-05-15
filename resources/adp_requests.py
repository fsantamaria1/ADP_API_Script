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

    def generate_employee_api_urls(self, top: int, skip: int):
        """
        Generates a list of URLs for retrieving employee data.
        :param skip: The number of pages/records to skip
        :param top: The number of pages/records to retrieve
        :return: A list of URLs for retrieving employee data.
        """

        # Make the URL for the API call
        employee_url = (
            f"{self.employee_api_endpoint}?"
            f"$top={top}&"
            f"$skip={skip}"
        )
        return employee_url

    def generate_timecard_api_urls(self, top: int, skip: int, start_date, main_associate_id: str):
        """
        Generates a list of URLs for retrieving timecard data.
        :param skip: The number of pages/records to skip
        :param top: The number of pages/records to retrieve
        :param start_date: The start date for the timecard data.
        :param main_associate_id: The ID of the associate id used to retrieve all the team time cards.
        :return: A list of URLs for retrieving timecard data.
        """

        # Specify query parameters for the API call
        api_route = "team-time-cards"
        expand_param = "dayEntries"
        filter_param = f"timeCards/timePeriod/startDate eq '{start_date}'"

        # Make the URL for the API call
        time_card_final = (
            f"{self.timecard_api_endpoint}/"
            f"{main_associate_id}/"
            f"{api_route}?"
            f"$expand={expand_param}&"
            f"$top={top}&"
            f"$skip={skip}&"
            f"$filter={filter_param}"
        )
        return time_card_final


class APIConnector:
    """
    Class for connecting to the ADP API and retrieving data.
    """

    def __init__(self, full_certificate: tuple, base_64_credentials):
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

    def get_time_cards(self, main_associate_id, start_date):
        """
        Retrieves a list of time cards from the ADP API.
        :param main_associate_id: The associate ID of the main employee to retrieve their team time cards.
        :param start_date: The pay period start date. It is always a Monday's date and in this format: YYYY_MM-DD
        :return: A list of JSONs which contain time card information
        """
        self.verify_token()
        list_of_time_cards = []

        # Pagination
        top = 25
        skip = 0

        try:
            headers = {
                'Authorization': self.token,
                'Accept-Encoding': 'gzip, deflate',
                'Host': self.api_host,
                'Connection': 'Keep-Alive',
                'User-Agent': 'Apache-HttpClient/4.5.2(Java/1.8.0_112)',
                'Accept': 'application/json',
                'Cookie': 'BIGipServerp_dc1_mobile_sor_integratedezlm=3938124043.15395.0000; BIGipServerp_dc2_mobile_apache_sor=3013608203.5377.0000; BIGipServerp_mkplproxy-dc1=1633878283.20480.0000; BIGipServerp_mkplproxy-dc2=670892811.20480.0000; BIGipServerp_dc1_mobile_apache_sor=153042955.5377.0000; Cookie_1=value'
            }
            while True:
                time_card_url = self.url_generator.generate_timecard_api_urls(top, skip, start_date, main_associate_id)
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
                        # Change the range of pages
                        skip += 25

                    else:
                        response.raise_for_status()

        except Exception as e:
            logging.error(f"An error occurred while retrieving time cards.\n Error: {str(e)}\n")
            raise

    def get_employees(self):
        """
        Retrieves a list of employees from the ADP API.
        :return: A list of employees in JSON format.
        """

        self.verify_token()
        list_of_employees = []

        # Pagination
        top = 50
        skip = 0

        try:

            headers = {
                'Authorization': self.token,
                'Cookie': 'BIGipServerp_dc1_mobile_apache_sor=706691083.5377.0000; BIGipServerp_mkplproxy-dc1=2803368203.20480.0000; BIGipServerp_mkplproxy-dc2=654115595.20480.0000'
            }
            while True:
                employee_url = self.url_generator.generate_employee_api_urls(top, skip)
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

                        # Change the range of pages
                        skip += 50

                    elif response.status_code == 204:
                        break

                    else:
                        response.raise_for_status()

            return list_of_employees

        except Exception as e:
            logging.error(
                f"An error occurred while retrieving employees.\n Error: {str(e)}\n")
            raise
