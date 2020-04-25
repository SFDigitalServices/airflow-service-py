#pylint: disable=duplicate-code
"""Test functions from modules/citytest_sf_appointments"""
import json
from unittest.mock import patch
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
        'applicantWillDrive': 'yes',
        'acuityId': 372424060,
        'appointmentDatetime': '2020-04-17T16:00:00-0700',
        'acuityCreatedTime': '2020-04-15T20:17:59-0500',
        'formioId': None,
        'calendarID': 3838867
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
        'pcpFieldSetIagreetosharemyinformationwithKaiser': None,
        'dsw': '000000',
    }

    assert expected_appt.items() <= appt.items()

# Contractor appts

def test_parse_formio_response_listed_employer():
    """Test formatting a sample contractor form.io response with a listed employer. """
    with open(
            'airflow_home/dags/tests/mocks/formio_contractor_listed_company_parents_insurance.json',
            'r'
        ) as appt_file:
        mock_appt = json.load(appt_file)
        appt = CityTestSFAppointments.parse_formio_response(mock_appt)
    assert appt['employer'] == 'AMR'

def test_parse_formio_response_unlisted_employer():
    """Test formatting a sample contractor form.io response with a unlisted employer. """
    with open(
            'airflow_home/dags/tests/mocks/formio_contractor_unlisted_company_self_insured.json',
            'r'
        ) as appt_file:
        mock_appt = json.load(appt_file)
        appt = CityTestSFAppointments.parse_formio_response(mock_appt)
    assert appt['employer'] == 'My other employer'

def test_parse_formio_response_identity():
    """Verify identity info is parsed correctly from sample contractor form.io response. """
    with open(
            'airflow_home/dags/tests/mocks/formio_contractor_unlisted_company_self_insured.json',
            'r'
        ) as appt_file:
        mock_appt = json.load(appt_file)
        appt = CityTestSFAppointments.parse_formio_response(mock_appt)
    assert appt['panelFieldsetYourdateofbirth'] == '01/12/1920'
    assert appt['panelFieldsetYourethnicity'] == 'white'
    assert appt['panelFieldsetYoursexatbirth'] == 'm'
    assert appt['middleName'] == 'J'

def test_parse_formio_response_address():
    """Verify address info is parsed correctly from sample contractor form.io response. """
    with open(
            'airflow_home/dags/tests/mocks/formio_contractor_unlisted_company_self_insured.json',
            'r'
        ) as appt_file:
        mock_appt = json.load(appt_file)
        appt = CityTestSFAppointments.parse_formio_response(mock_appt)
    assert appt['homeAddress'] == '123 Main st'
    assert appt['homeCity'] == 'Berkeley'
    assert appt['homeState'] == 'CA'
    assert appt['homeZipcode'] == '94703'

def test_parse_formio_worksite_address():
    """Verify worksite address info is parsed correctly from sample contractor form.io response. """
    with open(
            'airflow_home/dags/tests/mocks/formio_contractor_unlisted_company_self_insured.json',
            'r'
        ) as appt_file:
        mock_appt = json.load(appt_file)
        appt = CityTestSFAppointments.parse_formio_response(mock_appt)
    expected_address = {
        'workAddress': '1231 Stevenson St',
        'workCity': 'San Francisco',
        'workState': 'CA',
        'workZipcode': '94103'
    }
    assert expected_address.items() <= appt.items()

def test_parse_formio_insurance_primary_holder_self():
    """Verify insurance info is parsed correctly if the primary insurance holder is self. """
    with open(
            'airflow_home/dags/tests/mocks/formio_contractor_unlisted_company_self_insured.json',
            'r'
        ) as appt_file:
        mock_appt = json.load(appt_file)
        appt = CityTestSFAppointments.parse_formio_response(mock_appt)

    expected_insurance = {
        'healthInsuranceIdNumber': 'insurance id',
        'healthInsuranceGroupIdNumber': 'group id',
        'primaryHolderHealthInsurance': 'self'
    }
    assert expected_insurance.items() <= appt.items()


def test_parse_formio_insurance_primary_holder_parent():
    """Verify insurance info is parsed correctly if the primary insurance holder is a parent. """
    with open(
            'airflow_home/dags/tests/mocks/formio_contractor_listed_company_parents_insurance.json',
            'r'
        ) as appt_file:
        mock_appt = json.load(appt_file)
        appt = CityTestSFAppointments.parse_formio_response(mock_appt)

    expected_insurance = {
        'healthInsuranceIdNumber': 'insurance id number',
        'healthInsuranceGroupIdNumber': 'group id number',
        'primaryHolderHealthInsurance': 'parent',
        'primaryHolderHealthInsuranceFirstname': 'Parental',
        'primaryHolderHealthInsuranceLastname': 'unit'
    }
    assert expected_insurance.items() <= appt.items()

def test_get_formio_id_by_email():
    """ Verify Form.io ID query by email """
    with open(
            'airflow_home/dags/tests/mocks/formio_contractor_unlisted_company_self_insured.json',
            'r'
        ) as appt_file:
        mock_appt = json.load(appt_file)
        mock_appts = [mock_appt]

        with patch('modules.formio.Formio.get_formio_submission_by_query') as mock:
            mock.return_value = mock_appts
            formio_id = CityTestSFAppointments.get_formio_id_by_email(
                "testWithUnlistedEmployer@test.com")

    assert formio_id == "5e98b5cdcc554a79aa0e7524"
