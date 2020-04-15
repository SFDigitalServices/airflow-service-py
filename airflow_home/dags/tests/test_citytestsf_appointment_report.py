""" Test CityTestSF Appointment Report script """
from unittest.mock import patch
from scripts.citytestsf_appointment_report import refresh_appointment_data

def test_refresh_appointment_data():
    """Test refresh_appointment_data"""
    with patch('pygsheets.Worksheet.clear') as mock_clear:
        mock_clear.return_value = None
        with patch('pygsheets.Worksheet.insert_rows') as mock_insert_rows:
            mock_insert_rows.return_value = None
            data = refresh_appointment_data(task_instance=MockTaskInstance())
    assert isinstance(data, int)

#pylint: disable=too-few-public-methods
class MockTaskInstance:
    """ Mock OOC Task Instance """
    @staticmethod
    def xcom_push(key, value):
        """ mock xcom_push """
        if key == 'appointment_report':
            assert value
        else:
            assert False
