#pylint: disable=duplicate-code
"""Test functions from modules/citytest_sf_appointments"""
import json
from modules.citytest_sf_appointments import CityTestSFAppointments

def test_format_acuity_appointment():
    """Test formatting a sample canceled acuity appointment. """
    with open(
            'airflow_home/dags/tests/mocks/acuity_canceled_appointment_without_formio_id.json',
            'r'
        ) as appt_file:
        mock_appt = json.load(appt_file)
        appt = CityTestSFAppointments.parse_appointment(mock_appt)

    expected_acuity_appt = {
        'firstName': 'test',
        'lastName': 'test',
        'phone': '9783020023',
        'email': 'andrea.egan@sfgov.org',
        'canceled': True,
        'dsw': '000000',
        'applicantWillDrive': 'yes',
        'acuityId': 372424060,
        'appointmentDatetime': '2020-04-17T16:00:00-0700',
        'acuityCreatedTime': '2020-04-15T20:17:59-0500',
        'formioId': None
    }
    assert appt == expected_acuity_appt
    assert appt['formioId'] is None


def test_format_acuity_appointment_with_formio_id():
    """Test formatting a sample canceled acuity appointment. """
    with open(
            'airflow_home/dags/tests/mocks/acuity_appointment_with_formio_id.json',
            'r'
        ) as appt_file:
        mock_appt = json.load(appt_file)
        appt = CityTestSFAppointments.parse_appointment(mock_appt)

    assert appt['formioId'] == '5e9892399e7436203dfe7250'


def test_parse_formio_response():
    """Test formatting a sample form.io response without a pcp. """
    with open('airflow_home/dags/tests/mocks/formio_response_no_pcp.json', 'r') as appt_file:
        mock_appt = json.load(appt_file)
        appt = CityTestSFAppointments.parse_formio_response(mock_appt)

    expected_appt = {
        'formioId': '5e97b23b49ccf626cb5dff6d',
        'formioSubmittedTime': '2020-04-16T01:17:47.677Z',
        'hasNoPCP': True,
        'lastReportedWorkDate': '04/15/2020',
        'insuranceCarrier': 'United Healthcare',
        'kaiserMedicalRecordNumber': None,
        'pcpFieldSetIagreetosharemyinformationwithKaiser': None
    }

    assert appt == expected_appt
