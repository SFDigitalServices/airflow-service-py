"""Functions related to interacting with Acuity Scheduling."""
import os

from datetime import date
from urllib.parse import urljoin
import requests
from requests.auth import HTTPBasicAuth

from modules.core import Core

class Acuity(Core):
    """Functions related to interacting with Acuity Scheduling."""
    @staticmethod
    #pylint: disable=too-many-arguments
    def get_appointments_by_type(
            base_url=os.environ.get('ACUITY_BASE_URL'),
            appt_type=os.environ.get('ACUITY_APPT_TYPE'),
            user=os.environ.get('ACUITY_USER'),
            pwd=os.environ.get('ACUITY_PASSWORD'),
            start_date=date.today(),
            end_date=date.today(),
            max_records=1000
        ):
        """Get Acuity appts based on the appt type and the option to filter by day."""
        url = urljoin(base_url, '/api/v1/appointments')
        params = {
            'appointmentTypeID': appt_type,
            'canceled': False,
            'max': max_records
        }

        if start_date:
            params['minDate'] = start_date.strftime('%Y-%m-%d')
        if end_date:
            params['maxDate'] = end_date.strftime('%Y-%m-%d')


        response = requests.get(
            url,
            auth=HTTPBasicAuth(user, pwd),
            params=params
        )

        response.raise_for_status()

        return response.json()

    @staticmethod
    def get_appointment(
            appt_id,
            base_url=os.environ.get('ACUITY_BASE_URL'),
            user=os.environ.get('ACUITY_USER'),
            pwd=os.environ.get('ACUITY_PASSWORD')
        ):
        """Get a single Acuity appointment given an appointment Id. """
        url = urljoin(base_url, '/api/v1/appointments/{}'.format(appt_id))

        response = requests.get(
            url,
            auth=HTTPBasicAuth(user, pwd),
        )

        response.raise_for_status()

        return response.json()
