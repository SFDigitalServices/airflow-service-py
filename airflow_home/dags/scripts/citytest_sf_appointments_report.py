""" CityTestSF Appointment Report script """
import os
import base64
import datetime
from datetime import date
import sentry_sdk
import pygsheets
from modules.citytest_sf_appointments_report import CityTestSFAppointmentsReport

def refresh_appointment_data(**context):
    """ refresh_appointment_data """

    # Get appointments from Acuity
    appts = get_appointments_from_acuity(**context)
    # Prepare to Google Sheets
    data = prep_data_for_report(appts)
    # Upload to Google
    upload_data_to_google(data)

    sentry_sdk.capture_message(
        """
        citytestsf.appointments_report.complete with {} rows"""
        .format(len(data)), 'info')

    return len(data)

def get_appointments_from_acuity(**context):
    """Get appointments from acuity."""
    start_date = date.today() - datetime.timedelta(days=1)
    end_date = date.today() + datetime.timedelta(days=7)

    sentry_sdk.capture_message(
        """
        citytestsf.appointments_report.get_appointments_from_acuity from {start_data} to {end_date}.
        """.format(
            start_data=start_date,
            end_date=end_date
        ), 'info')

    appointments = CityTestSFAppointmentsReport.get_acuity_appointments(
        start_date,
        end_date)
    parsed_appointments = [
        CityTestSFAppointmentsReport.parse_appointment(
            appt,
            ["appointmentTypeID", "calendar", "calendarID"])
        for appt in appointments]

    task_instance = context['task_instance']
    task_instance.xcom_push(key="num_appointments", value=len(parsed_appointments))

    return parsed_appointments

def prep_data_for_report(data):
    """ Prepare Data for Report """
    data_list = []
    fields = [
        "acuityId",
        "appointmentTypeID",
        "applicantWillDrive",
        "appointmentDatetime",
        "acuityCreatedTime",
        "calendar",
        "calendarID",
        "formioId"
        ]
    header = map(lambda x: x.upper(), fields)
    data_list.append(list(header))

    for appt in data:
        row = []
        if not CityTestSFAppointmentsReport.is_test_appt(appt):
            for field in fields:
                value = appt[field]
                row.append(value)
            data_list.append(row)

    sentry_sdk.capture_message(
        """
        citytestsf.appointments_report.prep_data_for_report for {rows_length} rows.
        """.format(
            rows_length=len(data_list)
        ), 'info')

    return data_list

def upload_data_to_google(data):
    """ Uploads Appointment Data to Google Sheets """

    sentry_sdk.capture_message(
        """
        citytestsf.appointments_report.upload_data_to_google.start
        """, 'info')

    cred = base64.b64decode(os.environ.get('AIRFLOW_GOOGLE_API_64')).decode('ascii')
    os.environ['CITYTEST_SHEET_API'] = cred
    client = pygsheets.authorize(service_account_env_var='CITYTEST_SHEET_API')

    sheet = client.open_by_key(os.environ['CITYTEST_REPORT_SHEET'])
    google_sheet = os.environ['CITYTEST_REPORT_LIST']
    worksheet = sheet.worksheet('title', google_sheet)
    if len(data) > 0:
        worksheet.clear()
        worksheet.resize(10)
        worksheet.insert_rows(0, number=len(data), values=data)

    sentry_sdk.capture_message(
        """
        citytestsf.appointments_report.upload_data_to_google {rows_length} rows.
        """.format(
            rows_length=len(data)
        ), 'info')

    return len(data)
