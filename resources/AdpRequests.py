class UrlGenerator:
    """
       Helper class for generating URLs for ADP API calls.
       """

    def __init__(self):

        # Endpoints for API calls
        self.timecard_api_endpoint = "https://api.adp.com/time/v2/workers"
        self.employee_api_endpoint = "https://api.adp.com/hr/v2/workers"

    @staticmethod
    def generate_api_url(api_endpoint, top, skip, args=None):
        """
                Generates an API URL with the specified parameters.

                Args:
                    api_endpoint (str): The base URL for the API.
                    top (int): The number of records to retrieve.
                    skip (int): The number of records to skip.
                    args (str): Additional parameters for the API call.

                Returns:
                    str: The complete URL for the API call.
                """
        if args is not None:
            return f"{api_endpoint}/{args}$top={top}&$skip={skip}"
        else:
            return f"{api_endpoint}?$top={top}&$skip={skip}"

    def generate_employee_api_urls_(self, max_number_of_records):
        """
                Generates a list of URLs for retrieving employee data.

                Args:
                    max_number_of_records (int): The maximum number of records to retrieve.

                Returns:
                    list: A list of URLs for retrieving employee data.
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

    def generate_timecard_api_urls(self, max_number_of_records, start_date, main_associate_id):
        """
                Generates a list of URLs for retrieving timecard data.

                Args:
                    max_number_of_records (int): The maximum number of records to retrieve.
                    start_date (str): The start date for the timecard data.
                    main_associate_id (str): The ID of the associate id used to retrieve all the team time cards.

                Returns:
                    list: A list of URLs for retrieving timecard data.
                """
        processed = 0
        top = 25
        skip = 0
        list_of_time_card_urls = []
        rest_of_url = f"{main_associate_id}/team-time-cards?$expand=dayEntries&"
        while processed <= max_number_of_records:
            time_card_url = self.generate_api_url(self.timecard_api_endpoint, top, skip, rest_of_url)
            time_card_url = f"{time_card_url}&$filter=timeCards/timePeriod/startDate eq '{start_date}'"
            print(time_card_url)
            list_of_time_card_urls.append(time_card_url)
            skip += 25
            processed += 25
        return list_of_time_card_urls
