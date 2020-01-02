""" Test OOC proposal Retail script """
import json
from unittest.mock import patch
from scripts.ooc_proposed_retail import pull_from_screendoor, push_to_datasf

class MockOOCTaskInstance:
    """ Mock OOC Task Instance """
    @staticmethod
    def xcom_push(key, value):
        """ mock xcom_push """
        assert key == 'proposed_retail_list'
        assert len(value) > 0
        row = value[0]
        assert list(row.keys()) == ['dba_name', 'address', 'parcel', 'activities', 'status']

    @staticmethod
    def xcom_pull(task_ids, key):
        """ mock xcom_pull """
        assert key == 'proposed_retail_list'
        assert task_ids == 'pull_from_screendoor'
        data = [{'undefined_field':'test'}]
        return data

def test_pull_from_screendoor():
    """ Test pull_from_screendoor """
    with open('airflow_home/dags/tests/mocks/ooc_sd_responses.json', 'r') as file_obj:
        mock_responses = json.load(file_obj)

    assert mock_responses

    with patch('screendoor_sdk.screendoor.Screendoor.get_project_responses') as mock:
        mock.return_value = mock_responses
        resp = pull_from_screendoor(task_instance=MockOOCTaskInstance())
    assert resp

def test_push_to_datasf():
    """ Test push_to_datasf """
    mock_return = 'test_push_to_datasf'
    with patch('sodapy.Socrata.replace') as mock:
        mock.return_value = mock_return
        resp = push_to_datasf(task_instance=MockOOCTaskInstance())
    assert resp == mock_return
