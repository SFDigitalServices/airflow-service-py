# pylint: disable=fixme
"""Functions related to interacting with Form.io forms."""
import os
import requests

from modules.core import Core

# pylint: disable=too-few-public-methods
class Formio(Core):
    """Functions related to interacting with Form.io forms."""
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

    @staticmethod
    #pylint: disable=too-many-arguments
    def get_formio_submissions(
            form_id=os.environ.get('FORMIO_FORM_ID'),
            base_url=os.environ.get('FORMIO_BASE_URL'),
            formio_api_key=os.environ.get('FORMIO_API_KEY'),
            select_fields=','.join(default_select_fields),
            dsw_ids=None,
            limit=500
        ):
        """Get form.io submissions with the option of filtering by DSWs."""
        headers = {
            'x-token': '{}'.format(formio_api_key),
            'Content-Type': 'application/json'
        }
        formio_url = '{base_url}/form/{form_id}/{submission_endpoint}'.format(
            base_url=base_url,
            form_id=form_id,
            submission_endpoint='submission'
        )

        # FIXME-set limit based on length of dsws and limit length of dsws to max 2048 query string
        params = {'limit': limit}
        if select_fields:
            params['select'] = select_fields
        if dsw_ids:
            params['data.dsw__in'] = ','.join(dsw_ids)

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
        return response.json()

    @staticmethod
    def get_formio_submission_by_id(
            submission_id,
            form_id=os.environ.get('FORMIO_FORM_ID'),
            base_url=os.environ.get('FORMIO_BASE_URL'),
            formio_api_key=os.environ.get('FORMIO_API_KEY'),
        ):
        """Given a formio id, retreive a submission"""
        headers = {
            'x-token': '{}'.format(formio_api_key),
            'Content-Type': 'application/json'
        }

        url = '{base_url}/form/{form_id}/{submission_endpoint}/{submission_id}'.format(
            base_url=base_url,
            form_id=form_id,
            submission_endpoint='submission',
            submission_id=submission_id
        )

        response = requests.get(
            url,
            headers=headers
        )
        response.raise_for_status()

        return response.json()
