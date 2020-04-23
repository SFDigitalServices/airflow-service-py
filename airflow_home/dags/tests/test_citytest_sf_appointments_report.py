""" Test CityTestSF Appointment Report script """
# pylint: disable=line-too-long,unnecessary-pass,unused-import,too-few-public-methods,unused-argument
import json
from unittest.mock import patch
from scripts.citytest_sf_appointments_report import refresh_appointment_data, get_appointments_from_acuity, prep_data_for_report, upload_data_to_google

def test_refresh_appointment_data():
    """ Test refresh_appointment_data """
    pass

def test_get_appointments_from_acuity():
    """ Test get_appointments_from_acuity """
    pass

def test_prep_data_for_report():
    """ Test prep_data_for_report """
    pass

def test_upload_data_to_google():
    """ Test upload_data_to_google """
    with open('airflow_home/dags/tests/mocks/citytest_sf_report_google_data.json', 'r') as file_obj:
        mock_data = json.load(file_obj)

    assert mock_data

    with patch('pygsheets.authorize') as mock_authorize:
        mock_authorize.return_value = MockClient()
        data = upload_data_to_google(mock_data)
    assert data

class MockTaskInstance:
    """ Mock Task Instance """
    @staticmethod
    def xcom_push(key, value):
        """ mock xcom_push """
        assert key
        assert value

class MockClient:
    """ Mock client """
    @staticmethod
    def open_by_key(key):
        """ open_by_key method """
        assert key
        return MockSpreadsheet()

class MockSpreadsheet:
    """ Mock Spreadsheet """
    @staticmethod
    def worksheet(_property='index', _value=0):
        """ worksheet method """
        return MockWorksheet()

class MockWorksheet:
    """ Mock Worksheet """
    @staticmethod
    def clear():
        """ clear method """
        return True

    @staticmethod
    def insert_rows(row, number=1, values=None, inherit=False):
        """ insert_rows """
        return True

    @staticmethod
    def resize(rows=None, cols=None):
        """ resize """
        return True
