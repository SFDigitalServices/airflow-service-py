""" Acuity module"""
#pylint: disable=too-few-public-methods
from urllib.parse import urljoin
import requests
from modules.core import Core

class Acuity(Core):
    """Acuity class"""

    API_URL = "https://acuityscheduling.com/api/"

    def __init__(self, version="v1"):
        super().__init__()
        self.base_url = urljoin(self.API_URL, version)+"/"
        self.auth_cred = None

    def auth(self, user, pwd):
        """ auth method """
        self.auth_cred = requests.auth.HTTPBasicAuth(user, pwd)

    def get_appointments(self, params):
        """ get_appointments method """
        url = urljoin(self.base_url, 'appointments')

        response = requests.get(
            url,
            auth=self.auth_cred,
            params=params
        )

        response.raise_for_status()

        return response.json()
