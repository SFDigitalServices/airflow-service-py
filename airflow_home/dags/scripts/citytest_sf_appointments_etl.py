""" OOC Proposed Retail script """
import os
import requests
import sentry_sdk

import requests
from requests.auth import HTTPBasicAuth
from urllib.parse import urljoin
import datetime
from datetime import date
import csv
import collections
import pytz
import json

from modules.formio import Formio
from modules.acuity import Acuity
from modules.citytest_sf_appointments import CityTestSFAppointments


def pull_from_acuity(**context):
    """ pull appointments from acuity """
    print('starting pull_from_acuity')
    # sentry_sdk.capture_message('citytest_sf.appointments.pull_from_acuity.init', 'info')
    pacific = pytz.timezone('US/Pacific')
    today = pacific.localize(datetime.datetime.today())
    tomorrow = (today + datetime.timedelta(days=1))

    # Get Acuity appointments and parse
    acuity = Acuity()
    citytest = CityTestSFAppointments()
    appointments = acuity.get_appointments_by_type(start_date=tomorrow, end_date=tomorrow)
    parsed_appointments = [citytest.parse_appointment(appt) for appt in appointments]

    # Filter out first name "test"
    parsed_appointments = [appt for appt in parsed_appointments if appt['firstName'].lower() != 'test']

    # sentry_sdk.capture_message(
    #     'citytest_sf.appointments.pull_from_acuity.num_appointments: {}'.format(
    #         len(parsed_appointments)
    #     ),
    #     'info'
    # )

    # Log duplicate appointments
    # sentry_sdk.capture_message(
    #     'citytest_sf.appointments.pull_from_acuity.duplicates: {}'.format(
    #         check_for_appt_duplicates(parsed_appointments)
    #     ),
    #     'warning'
    # )

    dsws = [appt['dsw'] for appt in parsed_appointments if appt['dsw']]

    # Save data
    task_instance = context['task_instance']
    task_instance.xcom_push(key="dsws", value=dsws)
    task_instance.xcom_push(key="parsed_appointments", value=parsed_appointments)
    print('ending pull_from_acuity', len(parsed_appointments), bool(parsed_appointments))

    return bool(parsed_appointments)

def merge_with_formio(**context):
    """Get form.io responses for provided dsws, merge data together """
    print('starting merge_with_formio')
    # sentry_sdk.capture_message('citytest_sf.appointments.merge_with_formio.init', 'info')

    dsws= context['task_instance'].xcom_pull(
        task_ids='pull_from_acuity', key='dsws')

    parsed_appointments = context['task_instance'].xcom_pull(
        task_ids='pull_from_acuity', key='parsed_appointments')

    formio = Formio()
    citytest = CityTestSFAppointments()
    parsed_formio_responses = dict([citytest.parse_formio_response(r) for r in formio.get_formio_submissions(dsw_ids=dsws)])

    # sentry_sdk.capture_message(
    #     'citytest_sf.appointments.merge_with_formio.num_formio: {}'.format(
    #         len(parsed_formio_responses)
    #     ),
    #     'info'
    # )

    # Merge them together on DSW
    final_appointments = citytest.merge_acuity_formio(parsed_appointments, parsed_formio_responses)

    context['task_instance'].xcom_push(key='final_appointments', value='final_appointments')
    print('ending merge_with_formio', len(final_appointments), final_appointments[0])

    return bool(final_appointments)

def send_to_color(**context):
    """Send data to Color over SFTP."""

    appointments = context['task_instance'].xcom_pull(
        task_ids='merge_with_formio', key='final_appointments')

    print('final appointments?', len(appointments), appointments[0])

    return bool(appointments)
    # FIXME: Add stuff here.
    # notified = False

    # notify_url = os.environ['OOC_WEB_NOTIFY']

    # if notify_url:
    #     response = requests.get(notify_url)
    #     notified = response.status_code

    #     task_instance = context['task_instance']
    #     task_instance.xcom_push(key="notify_website_response", value=response.text)

    # return notified