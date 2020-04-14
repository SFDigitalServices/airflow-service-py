import requests
import os

import sentry_sdk

from modules.core import Core

class Formio(Core):

    def __init__(self):
        super().__init__()
        self.base_url = os.environ.get('FORMIO_BASE_URL')
        self.api_key = os.environ.get('FORMIO_API_KEY')
        self.form_id = os.environ.get('FORMIO_FORM_ID')

    default_select_fields = [
        'data.kaiserMedicalRecordNumber',
        'data.pcpFieldSetIagreetosharemyinformationwithKaiser',
        'data.dsw',
        'created',
        'data.lastReportedWorkDate',
        'data.insuranceCarrier',
        'data.hasPCP',
        'data.pcp'
    ]

    def get_formio_submissions(
            self,
            form_id=os.environ.get('FORMIO_FORM_ID'),
            base_url=os.environ.get('FORMIO_BASE_URL'),
            formio_api_key=os.environ.get('FORMIO_API_KEY'),
            select_fields=','.join(default_select_fields),
            dsw_ids=None,
            limit=500
        ):

        headers = {
            'x-token': '{}'.format(formio_api_key),
            'Content-Type': 'application/json'
        }
        formio_url = '{base_url}/form/{form_id}/{submission_endpoint}'.format(
            base_url=base_url,
            form_id=form_id,
            submission_endpoint='submission'
        )

        # FIXME - set limit based on length of dsws and limit length of dsws to max 2048 query string
        params = {'limit': limit}
        if select_fields: params['select'] = select_fields
        if dsw_ids: params['data.dsw__in'] = ','.join(dsw_ids)

        try:
            response = requests.get(
                formio_url,
                headers=headers,
                params=params
            )
            response.raise_for_status()
        except requests.HTTPError:
            print('Error with formio request: ', response.text)
            raise
            return False
        return response.json()