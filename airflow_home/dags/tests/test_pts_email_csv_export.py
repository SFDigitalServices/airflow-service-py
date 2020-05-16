""" Test PTS Email CSV Export script """
import json
from unittest.mock import patch
from scripts.pts_email_csv_export import trigger_export

def test_pts_email_csv_export():
    """ Test pts_email_csv_export """
    with open('airflow_home/dags/tests/mocks/pts_email_csv_export_response.json', 'r') as file_obj:
        mock_responses = json.load(file_obj)

    assert mock_responses

    with patch('requests.get') as mock:
        mock.return_value = MockResponse(mock_responses, 200)
        resp = trigger_export()

        assert resp
        assert resp["data"]["responses"] == 1

# pylint: disable=too-few-public-methods
class MockResponse:
    """ Mock Reponse class """
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        """ json method """
        return self.json_data

    @staticmethod
    def raise_for_status():
        """ raise_for_status method """
        return True
