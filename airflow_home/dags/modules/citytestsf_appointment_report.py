"""CityTestSF Appointment Report module"""
import os
import base64
import datetime
from datetime import date
import pygsheets
import sentry_sdk
from modules.core import Core
from modules.acuity import Acuity

class Report(Core):
    """CityTestSF Appointment Report class"""

    GOOGLE_API_ENV = 'AIRFLOW_GOOGLE_API_64'

    def run(self):
        """ run method """
        cred = base64.b64decode(os.environ.get(self.GOOGLE_API_ENV)).decode('ascii')
        os.environ['CITYTEST_SHEET_API'] = cred
        client = pygsheets.authorize(service_account_env_var='CITYTEST_SHEET_API')

        sheet = client.open_by_key(os.environ['REPORT_SHEET'])
        google_sheet = os.environ['REPORT_LIST']
        worksheet = sheet.worksheet('title', google_sheet)

        appointments = self.get_acuity_appointments(
            datetime.datetime.strptime(os.environ['CITYTEST_START_DATE'], '%Y-%m-%d'),
            datetime.datetime.combine(date.today() + datetime.timedelta(days=7), datetime.time.min))

        parsed_appointments = [self.parse_appointment(appt) for appt in appointments]

        google_data = self.get_google()

        data = self.combine(parsed_appointments, google_data)

        if len(data) > 0:
            worksheet.clear()
            worksheet.insert_rows(0, number=len(data), values=data)

        return len(data)



    def combine(self, parsed_appointments, google_data):
        """ combine method """
        return_list = []
        fields = [
            "dsw",
            "DEPT",
            "firstName",
            "lastName",
            "phone",
            "email",
            "acuityId",
            "appointmentDatetime",
            "datetimeCreated",
            "appointmentTypeID"
        ]
        header = map(lambda x: x.upper(), fields)

        return_list.append(list(header))
        combine_exceptions = []
        #pylint: disable=too-many-nested-blocks
        for appt in parsed_appointments:
            row = []
            if not self.is_test_appt(appt):
                for field in fields:
                    if field == "DEPT":
                        data_id = appt["dsw"]
                        dept = ""
                        if data_id and data_id in google_data:
                            dept = google_data[data_id]['DEPT']
                        else:
                            if data_id:
                                combine_exceptions.append("Cannot find DEPT for "+str(data_id))
                            else:
                                combine_exceptions.append("Empty ID for "+str(appt["acuityId"]))
                        value = dept
                    else:
                        value = appt[field]
                    row.append(value)
                return_list.append(row)
            with sentry_sdk.configure_scope() as scope:
                scope.set_extra('combine_exceptions', combine_exceptions)

            sentry_sdk.capture_message(
                'citytestsf.appointment_report.combine', 'info')
        return return_list

    def get_google(self):
        """ get_google method """
        cred = base64.b64decode(os.environ.get(self.GOOGLE_API_ENV)).decode('ascii')
        os.environ['CITYTEST_SHEET_API'] = cred

        client = pygsheets.authorize(service_account_env_var='CITYTEST_SHEET_API')

        sheet = client.open_by_key(os.environ['CITYTEST_SHEET'])
        google_sheet = os.environ['CITYTEST_LIST']
        worksheet = sheet.worksheet('title', google_sheet)

        row_header = worksheet.get_row(1)

        matrix = worksheet.get_all_values()
        row_header = matrix.pop(0)
        id_index = row_header.index('ID')
        dept_index = row_header.index('DEPT')

        data = {}
        get_google_exceptions = []
        for row in matrix:
            data_id = self.get_id(row[id_index])
            if data_id:
                if data_id in data:
                    get_google_exceptions.append("Overwriting " + data_id)
                data[data_id] = {"DEPT": row[dept_index]}
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra('get_google_exceptions', get_google_exceptions)
        return data

    @staticmethod
    def get_acuity_appointments(start_date=date.today(), end_date=date.today()):
        """ get_acuity_appointments method """
        acuity = Acuity()
        acuity.auth(os.environ['ACUITY_USER'], os.environ['ACUITY_PWD'])
        appointments = []
        default_params = {
            'canceled': False,
            'max': 1100
        }
        types = os.environ['ACUITY_APPT_TYPES'].split(',')
        for appt_type in types:
            params = default_params
            params['appointmentTypeID'] = appt_type
            days = 2
            for idx in range(0, (end_date-start_date).days+1):
                if idx % days == 0:
                    params['minDate'] = (start_date
                                         + datetime.timedelta(days=idx)).strftime('%Y-%m-%d')
                    params['maxDate'] = (start_date
                                         + datetime.timedelta(days=idx+days-1)).strftime('%Y-%m-%d')
                    print(params)
                    new_appointments = acuity.get_appointments(params)
                    appointments += new_appointments
        return appointments

    def parse_appointment(self, appointment):
        """ parse_appointment method """
        dsw_field_id = 7514073
        dsw_form_id = 1368026
        top_level_fields = [
            'firstName',
            'lastName',
            'phone',
            'email',
            'datetime',
            'id',
            'datetimeCreated',
            'appointmentTypeID'
        ]
        # Filter to only keys that we want
        parsed = dict((k, appointment[k]) for k in top_level_fields if k in appointment)

        # Looks like next is the most performant way to do this search
        # https://stackoverflow.com/questions/8653516/python-list-of-dictionaries-search
        dsw_form = next(
            (item.get('values') for item in appointment['forms'] if item['id'] == dsw_form_id), [])
        dsw = next(
            (item.get('value') for item in dsw_form if item['fieldID'] == dsw_field_id), None)

        parsed['dsw'] = self.get_id(dsw) if dsw else None

        # Rename id and datetime
        parsed['acuityId'] = parsed.pop('id')
        parsed['appointmentDatetime'] = parsed.pop('datetime')

        return parsed

    @staticmethod
    def get_id(data_id):
        """ Get normalized ID """
        if data_id:
            return data_id.rjust(6, '0')
        return data_id

    @staticmethod
    def is_test_appt(appt):
        """ Is Test Appointment """
        return appt["firstName"].upper() == "FIRST"
