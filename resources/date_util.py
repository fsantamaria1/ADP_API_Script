from datetime import date, datetime, timedelta


class DateUtil:
    """
    This class provides various methods for performing date operations.
    """

    DATE_FORMAT = '%Y-%m-%d'

    @staticmethod
    def str_to_date(date_str):
        """
        Converts a string formatted as '%Y-%m-%d' to a datetime object.
        :param date_str: str: A string formatted as '%Y-%m-%d'
        :return: datetime: A datetime object
        """
        return datetime.strptime(date_str, DateUtil.DATE_FORMAT)

    @staticmethod
    def _get_monday_(some_date):
        """
        Returns the Monday of the week for the given date.
        :param some_date: datetime: A datetime object
        :return: datetime: A datetime object representing the Monday of the week for the given date.
        """
        return some_date - timedelta(days=some_date.weekday())

    @staticmethod
    def get_this_monday():
        """
        Returns the Monday of the current week.
        :return: A string object representing the Monday of the current week.
        """
        today = date.today()
        this_monday = DateUtil._get_monday_(today)
        return this_monday.strftime(DateUtil.DATE_FORMAT)

    @staticmethod
    def get_last_monday():
        """
        Returns the Monday of the previous week.
        :return: A string object representing the Monday of the previous week.
                """
        today = date.today()
        monday = DateUtil._get_monday_(today)
        last_sunday = monday - timedelta(days=1)
        last_monday = DateUtil._get_monday_(last_sunday)
        return last_monday.strftime(DateUtil.DATE_FORMAT)

    @staticmethod
    def get_mondays(num_weeks):
        """
        Returns a list of Monday dates for the past num_weeks weeks.
        :param num_weeks: int: The number of weeks for which to generate Monday dates.
        :return: List[str]: A list of the Monday dates formatted as '%Y-%m-%d'
        """
        today = datetime.today()
        prev_monday = DateUtil._get_monday_(today)
        monday_dates = []
        for i in range(num_weeks):
            monday_date = prev_monday - timedelta(weeks=i)
            monday_dates.append(monday_date)

        monday_dates.reverse()

        return [monday_date.strftime(DateUtil.DATE_FORMAT) for monday_date in monday_dates]

    @staticmethod
    def get_mondays_between_dates(start_date_str, end_date_str):
        """
        Returns a list of Monday dates between two given dates.
        :param start_date_str: str: A string formatted as '%Y-%m-%d'
        :param end_date_str: str: A string formatted as '%Y-%m-%d'
        :return: List[datetime]: A list of datetime objects representing the Monday dates between the two given dates.
        """
        start_date = DateUtil.str_to_date(start_date_str)
        end_date = DateUtil.str_to_date(end_date_str)
        start_monday = DateUtil._get_monday_(start_date)
        mondays = [start_monday.strftime(DateUtil.DATE_FORMAT)]
        while True:
            next_monday = start_monday + timedelta(days=7)
            if next_monday > end_date:
                break
            mondays.append(next_monday.strftime(DateUtil.DATE_FORMAT))
            start_monday = next_monday
        return mondays

    @staticmethod
    def get_today():
        """
        Returns today's date.
        :return: date: Today's date as a date object.
        """
        return date.today()
