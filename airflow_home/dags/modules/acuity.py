import os
import sentry_sdk

from datetime import date
import requests
from requests.auth import HTTPBasicAuth
from urllib.parse import urljoin

from modules.core import Core

class Acuity(Core):

    def __init__(self):
        super().__init__()
        self.base_url = os.environ.get('ACUITY_BASE_URL')
        self.appt_type = os.environ.get('ACUITY_APPT_TYPE')
        self.user = os.environ.get('ACUITY_USER')
        self.pwd = os.environ.get('ACUITY_PASSWORD')

    def get_appointments_by_type(
            self,
            base_url = os.environ.get('ACUITY_BASE_URL'),
            appt_type = os.environ.get('ACUITY_APPT_TYPE'),
            user = os.environ.get('ACUITY_USER'),
            pwd = os.environ.get('ACUITY_PASSWORD'),
            start_date=date.today(),
            end_date=date.today(),
            max_records=1000
        ):
        url = urljoin(base_url, '/api/v1/appointments')
        params={
            'appointmentTypeID': appt_type,
            'canceled': False,
            'max': max_records
        }

        if start_date: params['minDate'] = start_date.strftime('%Y-%m-%d')
        if end_date: params['maxDate'] = end_date.strftime('%Y-%m-%d')


        response = requests.get(
            url,
            auth=HTTPBasicAuth(user, pwd),
            params=params
        )

        response.raise_for_status()

        return response.json()


    def get_appointment(self, appt_id, base_url,user,pwd):
        url = urljoin(base_url, '/api/v1/appointments/{}'.format(appt_id))

        response = requests.get(
            url,
            auth=HTTPBasicAuth(user, pwd),
        )

        response.raise_for_status()

        return response.json()