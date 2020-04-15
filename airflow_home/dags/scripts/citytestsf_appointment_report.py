""" CityTestSF Appointment Report script """
import sentry_sdk
from modules.citytestsf_appointment_report import Report

def refresh_appointment_data(**context):
    """ refresh_appointment_data """
    appointment_report = Report()
    sentry_sdk.capture_message(
        'citytestsf.appointment_report.refresh.init', 'info')

    data = appointment_report.run()

    sentry_sdk.capture_message(
        'citytestsf.appointment_report.complete', 'info')

    task_instance = context['task_instance']
    task_instance.xcom_push(key="appointment_report", value=data)

    return data
