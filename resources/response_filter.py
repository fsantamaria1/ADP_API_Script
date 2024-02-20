import json
from datetime import date, datetime, timedelta, timezone
from resources.models import UnnormalizedEmployees, UnnormalizedTimecards


class Employee:
    associate_oid = ""
    worker_id = ""
    payroll_name = ""
    first_name = ""
    last_name = ""
    middle_name = ""
    location_code = ""
    loc_desc = ""
    dept_code = ""
    dept_desc = ""
    ce_name = ""
    ce_dept = ""
    worker_status = ""
    is_active = False
    termination_date = None
    hourly_rate = None

    def __init__(self, associate_oid, worker_id, payroll_name, first_name, last_name, middle_name, 
                location_code, loc_desc, dept_code, dept_desc, ce_name, ce_dept,
                worker_status, termination_date, hourly_rate):
        self.associate_oid = associate_oid
        self.worker_id = worker_id
        self.payroll_name = payroll_name
        self.first_name = first_name
        self.last_name = last_name
        self.middle_name = middle_name
        self.location_code = location_code
        self.loc_desc = loc_desc
        self.dept_code = dept_code
        self.dept_desc = dept_desc
        self.ce_name = ce_name
        self.ce_dept = ce_dept
        self.worker_status = worker_status
        self.hourly_rate = hourly_rate
        if termination_date != "":
            self.termination_date = datetime.strptime(termination_date, "%Y-%m-%d")
            if self.termination_date > datetime.today() - timedelta(days = 15):
                self.is_active = True
        else:
            self.is_active = True

    def __str__(self) -> str:
        out_string = "{0} \t {1} \t {2}, {3}, {4} \n   {5}, {6} \t {7}, {8} \n   {9}, {10}, {11}".format(self.associate_oid, self.payroll_name, self.first_name, self.last_name, self.middle_name,
        self.location_code, self.loc_desc, self.dept_code, self.dept_desc, self.ce_name, self.ce_dept, self.hourly_rate)
        
        if self.termination_date != None:
            out_string = "{0} \t {1} \t {2}, {3}, {4} \n   {5}, {6} \t {7}, {8} \n   {9}, {10} \t {11}, {12}".format(self.associate_oid, self.payroll_name, self.first_name, self.last_name, self.middle_name,
            self.location_code, self.loc_desc, self.dept_code, self.dept_desc, self.ce_name, self.ce_dept, self.termination_date, self.is_active)
        return out_string
        
    def __UnnormalizedEmployees__(self) -> UnnormalizedEmployees:
        return UnnormalizedEmployees(associate_id=self.associate_oid, worker_id=self.worker_id, payroll_name=self.payroll_name,
                                    first_name=self.first_name, last_name=self.last_name, middle_name=self.middle_name,
                                    location_code=self.location_code, location_description=self.loc_desc,
                                    department_code=self.dept_code, department_description=self.dept_desc,
                                    worker_status=self.worker_status, is_active=self.is_active,
                                    ce_code=self.ce_name, ce_department=self.ce_dept, hourly_rate=self.hourly_rate)


class TimeEntry:

    def __init__(self, entry_id: str, entry_date: date, clock_in: datetime, clock_out: datetime, pay_code: str, status_code: str, time_duration: str):
        self.entry_id = entry_id
        self.entry_date = entry_date
        self.clock_in = clock_in
        self.clock_out = clock_out
        self.pay_code = pay_code
        self.status_code = status_code
        self.time_duration = time_duration


class Timecard:

    eastern_time_zone = timezone(timedelta(hours=4), name="EDT")

    def __init__(self, timecard_id: str, associate_id: str, pay_period_start: date, pay_period_end: date, processing_status_code: str, has_exception: bool, time_entry: TimeEntry):
        self.timecard_id = timecard_id
        self.associate_id = associate_id
        self.pay_period_start = pay_period_start
        self.pay_period_end = pay_period_end
        self.timecard_date = time_entry.entry_date
        self.entry_id = time_entry.entry_id
        self.entry_date = time_entry.entry_date
        self.clock_in = time_entry.clock_in
        self.clock_out = time_entry.clock_out
        self.time_duration = time_entry.time_duration
        self.pay_code_name = time_entry.pay_code
        self.entry_status_code = time_entry.status_code
        self.processing_status_code = processing_status_code
        self.has_exception = has_exception

    # for debugging
    def __str__(self):
        return "{0},\t{1}\n   {2}  --  {3} \n\t {4}, {5}".format(self.associate_id, self.pay_code_name, self.clock_in.__str__(), self.clock_out.__str__(), self.entry_id, self.time_duration)

    def __UnnormalizedTimecards__(self) -> UnnormalizedTimecards:
        return UnnormalizedTimecards(# Timecard data
                                    timecard_id=self.timecard_id,
                                    associate_id=self.associate_id,
                                    timecard_status_code=self.processing_status_code,
                                    pay_period_start=self.pay_period_start,
                                    pay_period_end=self.pay_period_end,
                                    has_exceptions=self.has_exception,
                                    # Entry data
                                    entry_id=self.entry_id,
                                    entry_date=self.entry_date,
                                    clock_in=self.clock_in,
                                    clock_out=self.clock_out,
                                    entry_status_code=self.entry_status_code,
                                    pay_code_name=self.pay_code_name,
                                    time_duration=self.time_duration
            )


class ResponseFilter:
    """ 
    This bad boy Filters your Responses
    """

    # Employees \/

    @staticmethod
    def get_employees(response_list):
        """
        Returns a list of Unnormalized Employees
        response_list is a list of "workers" lists from an api response. 
        """

        adp_worker_list = []

        for worker_list in response_list:
            if "workers" in worker_list:
                for each_worker in worker_list["workers"]:
                    adp_worker_list.append(DataParser.filter_each_worker(each_worker).__UnnormalizedEmployees__())

        return adp_worker_list
                    

    # Employees /\

    # Timecards \/

    @staticmethod
    def get_timecards(response_list):
        """
        Returns a list of Unnormalized Timecards
        response_list is a list of dictionaries containing the "teamTimeCards" list
        """

        # [ { "teamTimeCards": [ { a timecard } ] } ]

        timecard_model_list = []

        for response_dict in response_list:
            if "teamTimeCards" in response_dict.keys():
                for one_employee_cards in response_dict["teamTimeCards"]:
                    temp_timecard_models = DataParser.create_timecard_list(one_employee_cards)
                    if temp_timecard_models != []:
                        timecard_model_list.extend(temp_timecard_models)
                    
        return timecard_model_list



    # Timecards /\


class DataParser:

    @staticmethod
    def filter_each_worker(worker_dict : dict):
        """
        Used internaly
        """

        associate_id = ""
        worker_id = ""
        payroll_name = ""
        first_name = ""
        last_name = ""
        middle_name = ""
        location_code = ""
        loc_desc = ""
        dept_code = ""
        dept_desc = ""
        ce_name = ""
        ce_dept = ""
        termination_date = ""
        worker_status = ""
        hourly_rate = None

        # associate_id
        if "associateOID" in worker_dict:
            associate_id = worker_dict["associateOID"]

        # worker_id
        if "workerID" in worker_dict:
            if "idValue" in worker_dict["workerID"]:
                worker_id = worker_dict["workerID"]["idValue"]

        # payroll, first, last, and middle_name
        if "person" in worker_dict:
            if "legalName" in worker_dict["person"]:
                legal_name_dict = worker_dict["person"]["legalName"]

                if "formattedName" in legal_name_dict:
                   payroll_name = legal_name_dict["formattedName"]

                if "givenName" in legal_name_dict:
                    first_name = legal_name_dict["givenName"]

                if "familyName1" in legal_name_dict:
                    last_name = legal_name_dict["familyName1"]

                if "middleName" in legal_name_dict:
                    middle_name = legal_name_dict["middleName"]

        # worker_status
        if "workerStatus" in worker_dict:
            if "statusCode" in worker_dict["workerStatus"]:
                if "codeValue" in worker_dict["workerStatus"]["statusCode"]:
                    worker_status = worker_dict["workerStatus"]["statusCode"]["codeValue"]
        
        # USE THE ONE WHERE primaryIndicator IS TRUE
        # location_code, loc_desc, dept_code, dept_desc, hourly_rate
        if "workAssignments" in worker_dict:
            for work_assignment in worker_dict["workAssignments"]:

                # Read only from the primary work assignment.
                #  ignore other assignments.
                if work_assignment["primaryIndicator"]:
                    if "homeWorkLocation" in work_assignment:
                        if "nameCode" in work_assignment["homeWorkLocation"]:
                            location_name_code_dict = work_assignment["homeWorkLocation"]["nameCode"]
                            location_code = DataParser.get_location_code(location_name_code_dict)
                            loc_desc = DataParser.get_loc_desc(location_name_code_dict)

                    if "assignedOrganizationalUnits" in work_assignment:
                        for each_assigned_organizational_unit in work_assignment["assignedOrganizationalUnits"]:
                            if "nameCode" in each_assigned_organizational_unit:
                                organizational_units_name_code_dict = each_assigned_organizational_unit["nameCode"]

                                #Code
                                temp_dept_code = DataParser.get_dept_code(organizational_units_name_code_dict)
                                if temp_dept_code != "":
                                    dept_code = temp_dept_code

                                #Desc
                                temp_dept_desc = DataParser.get_dept_desc(organizational_units_name_code_dict)
                                if temp_dept_desc != "":
                                    dept_desc = temp_dept_desc
                                    
                    # Get hourly rate
                    if "baseRemuneration" in work_assignment:
                        base_remuneration_dict = work_assignment["baseRemuneration"]
                        if "hourlyRateAmount" in base_remuneration_dict:
                            if "amountValue" in base_remuneration_dict["hourlyRateAmount"]:
                                hourly_rate = base_remuneration_dict["hourlyRateAmount"]["amountValue"]

        # ce_name, ce_dept
        if "customFieldGroup" in worker_dict:
            if "stringFields" in worker_dict["customFieldGroup"]:
                for string_field in worker_dict["customFieldGroup"]["stringFields"]:
                    
                    string_field_name_code = DataParser.get_string_field_name_code(string_field)
                    if string_field_name_code == "CE Code":
                        ce_name = DataParser.get_string_field_value(string_field)
                    elif string_field_name_code == "CE Department":
                        ce_dept = DataParser.get_string_field_value(string_field)

        # termination_date
        if "workerDates" in worker_dict:
            if "terminationDate" in worker_dict["workerDates"]:
                termination_date = worker_dict["workerDates"]["terminationDate"]

        return Employee(associate_id, worker_id, payroll_name, first_name, last_name, middle_name, location_code, 
                         loc_desc, dept_code, dept_desc, ce_name, ce_dept, worker_status, termination_date, hourly_rate)

    @staticmethod
    def get_location_code(location_name_code_dict: dict):
        if "codeValue" in location_name_code_dict:
            return location_name_code_dict["codeValue"]
        else:
            return ""

    @staticmethod
    def get_loc_desc(location_name_code_dict: dict):
        if "shortName" in location_name_code_dict:
            return location_name_code_dict["shortName"]
        else:
            return ""

    @staticmethod
    def get_dept_code(organizational_units_dict: dict):
        if "codeValue" in organizational_units_dict:
            return organizational_units_dict["codeValue"]
        else:
            return ""

    @staticmethod
    def get_dept_desc(organizational_units_dict: dict):
        if "longName" in organizational_units_dict:
            return organizational_units_dict["longName"]
        elif "shortName" in organizational_units_dict:
            return organizational_units_dict["shortName"]
        else:
            return ""

    @staticmethod
    def get_string_field_name_code(string_field_dict: dict):
        if "nameCode" in string_field_dict:
            if "codeValue" in string_field_dict["nameCode"]:
                return string_field_dict["nameCode"]["codeValue"]
        return ""

    @staticmethod
    def get_string_field_value(string_field_dict: dict):
        if "stringValue" in string_field_dict:
            return string_field_dict["stringValue"]
        return ""

    @staticmethod
    def get_is_active(worker_status_dict: dict):
        if "codeValue" in worker_status_dict:
            if worker_status_dict["codeValue"] == "Terminated":
                return False
        return True

    # Employee /\

    # Timecard \/

    @staticmethod
    def create_timecard_list(response_timecard: dict):
        """
        Used internaly
        Filters a timecard dictionary to return a Timecard list
        response_timecard is a dictionary from the "teamTimeCard" list
        """

        if "timeCards" in response_timecard.keys():
            for one_timecard in response_timecard["timeCards"]:
                return DataParser.filter_timecard(one_timecard)


    @staticmethod
    def filter_timecard(timecard_dict: dict):
        """
        Used internaly
        Filters the "timeCards" list within a single item of "teamTimeCards"
        Returns a list 
        """

        timecard_model_list = []

        # The ingredients of a Timecard
        timecard_id = ""
        associate_id = ""
        processing_status_code = ""
        pay_period_start = date(2000, 1, 1)
        pay_period_end = date(2000, 1, 1)
        has_exception = False


        # timecard_id
        timecard_id = timecard_dict["timeCardID"]
        
        # associate_id
        associate_id = timecard_dict["associateOID"]

        # has_exception
        has_exception = timecard_dict["exceptionsIndicator"]

        # processing_status_code
        if "processingStatusCode" in timecard_dict.keys():
            if "codeValue" in timecard_dict["processingStatusCode"].keys():
                processing_status_code = timecard_dict["processingStatusCode"]["codeValue"]

        # pay_period start and end
        if "timePeriod" in timecard_dict.keys():
            time_period_dict = timecard_dict["timePeriod"]
            if "startDate" in time_period_dict.keys():
                pay_period_start = date.fromisoformat(time_period_dict["startDate"])
            if "endDate" in time_period_dict.keys():
                pay_period_end = date.fromisoformat(time_period_dict["endDate"])

        # Create TimeEntrys and Timecards
        if "dayEntries" in timecard_dict.keys():
            for day_entry in timecard_dict["dayEntries"]:
                if "timeEntries" in day_entry.keys():
                    for time_entry in day_entry["timeEntries"]:
                        # TimeEntry List
                        time_entrys = DataParser.filter_time_entries(time_entry)

                        for each_time_entry in time_entrys:
                            temp_timecard = Timecard(timecard_id, associate_id, pay_period_start, pay_period_end, processing_status_code, has_exception, each_time_entry)

                            # Turn Timecard into db model
                            timecard_model_list.append(
                                temp_timecard.__UnnormalizedTimecards__()
                                )
                else:
                    #no time entries
                    pass
        else:
            #no day entries
            pass

        return timecard_model_list


    @staticmethod
    def filter_time_entries(time_entries_dict: dict):
        """
        Used internaly
        Filters an item from "timeEntries"
        Returns a list of timeEntries
        """
        time_entry_list = []

        entry_id = ""
        entry_date = date(2000, 1, 1)
        clock_in = datetime(2000, 1, 1)
        clock_out = datetime(2000, 1, 1)
        status_code = ""
        pay_code = ""
        time_duration = ""
        
        # entry_id
        entry_id = time_entries_dict["entryID"]

        # entry_date
        if "entryDate" in time_entries_dict.keys():
            entry_date = date.fromisoformat(time_entries_dict["entryDate"])

        # start_period
        if "startPeriod" in time_entries_dict.keys():
            if "startDateTime" in time_entries_dict["startPeriod"].keys():
                clock_in = datetime.fromisoformat(time_entries_dict["startPeriod"]["startDateTime"])

        # end_period
        if "endPeriod" in time_entries_dict.keys():
            if "endDateTime" in time_entries_dict["endPeriod"].keys():
                clock_out = datetime.fromisoformat(time_entries_dict["endPeriod"]["endDateTime"])

        # status_code
        if "entryStatusCode" in time_entries_dict.keys():
            if "codeValue" in time_entries_dict["entryStatusCode"].keys():
                status_code = time_entries_dict["entryStatusCode"]["codeValue"]

        # pay_code and time_duration
        # it"s inside a list. Things might get messy if people work on a vacation day.
        if "entryTotals" in time_entries_dict.keys():
            for entry_total in time_entries_dict["entryTotals"]:
                if "payCode" in entry_total.keys():
                    if "codeValue" in entry_total["payCode"].keys():
                        pay_code = entry_total["payCode"]["codeValue"]
                if "timeDuration" in entry_total.keys():
                    time_duration = entry_total["timeDuration"]

                # Add each entry total as new TimeEntry
                temp_time_entry = TimeEntry(entry_id, entry_date, clock_in, clock_out, pay_code, status_code, time_duration)
                time_entry_list.append(temp_time_entry)

        # No entry totals. Just in case. 
        else:
            temp_time_entry = TimeEntry(entry_id, entry_date, clock_in, clock_out, pay_code, status_code, time_duration)
            time_entry_list.append(temp_time_entry)

        # exceptions
        #if "exceptions" in time_entries_dict.keys():
        #    for each_exception in time_entries_dict["exceptions"]:
        #        if "exceptionDescription" in each_exception.keys():
        #            exceptions.append(each_exception["exceptionDescription"])

        return time_entry_list
        
