""" DataSF module"""
#pylint: disable=too-few-public-methods
import os
import sentry_sdk
from sodapy import Socrata
from modules.core import Core

class DataSF(Core):
    """DataSF class"""
    def __init__(self):
        super().__init__()
        domain = 'data.sfgov.org'
        self.client = Socrata(domain, None)
        if os.environ.get('DATASF_KEY_ID'):
            self.client = Socrata(
                domain, None,
                username=os.environ.get('DATASF_KEY_ID'),
                password=os.environ.get('DATASF_KEY_SECRET'))

    def replace(self, name, data):
        """ replace method """
        data_id_name = 'DATASF_ID_' + name.upper()
        if os.environ.get(data_id_name):
            data_id = os.environ.get(data_id_name)
            try:
                resp = self.client.replace(data_id, data)
                with sentry_sdk.configure_scope() as scope:
                    scope.set_extra(name, {'data_id': data_id, 'length':len(data), 'resp':resp})
                sentry_sdk.capture_message('DataSF.sync.'+name, 'info')
                return resp
            #pylint: disable=broad-except
            except Exception as exception:
                sentry_sdk.capture_exception(exception)

        msg = 'Missing env variable: '+data_id_name
        sentry_sdk.capture_message(msg, 'error')
        return False
