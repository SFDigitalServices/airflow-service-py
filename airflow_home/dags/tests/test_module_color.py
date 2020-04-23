# pylint: disable=duplicate-code
"""Test functions from Color module."""
from modules.color import Color

SAMPLE_APPOINTMENT = {
    'firstName': 'test',
    'lastName': 'test',
    'phone': '4158675309',
    'email': 'test@sfgov.org',
    'dsw': '000000',
    'applicantWillDrive': 'yes',
    'canceled': False,
    'acuityId': 372213232,
    'appointmentDatetime': '2020-04-17T14:30:00-0700',
    'acuityCreatedTime': '2020-04-14T22:53:56-0500',
    'hasNoPCP': False,
    'formioSubmittedTime': '2020-04-15T03:53:41.893Z',
    'lastReportedWorkDate': '04/14/2020',
    'insuranceCarrier': 'United Healthcare',
    'kaiserMedicalRecordNumber': None,
    'pcpFieldSetIagreetosharemyinformationwithKaiser': None,
    'formioId': '5e9685450a8d6ff72109b87f',
    'pcpFirstName': 'doctor',
    'pcpLastName': 'doctor',
    'pcpPractice': 'hospital',
    'pcpCity': 'san francisco',
    'pcpState': 'CA',
    #pylint: disable=line-too-long
    'iAuthorizeColorToShareMyInformationAndTestResultsWithThePrimaryCarePhysicianIHaveIdentifiedOnThisFormForTreatmentAndCarePurposes': True
}

SAMPLE_CANCELED = {**SAMPLE_APPOINTMENT, **{'canceled': True}}

SAMPLE_WITHOUT_PCP = {
    'firstName': 'test',
    'lastName': 'test',
    'phone': '4158675309',
    'email': 'test@sfgov.org',
    'dsw': '000000',
    'applicantWillDrive': 'yes',
    'canceled': False,
    'acuityId': 372213232,
    'appointmentDatetime': '2020-04-17T14:30:00-0700',
    'acuityCreatedTime': '2020-04-14T22:53:56-0500',
    'formioId': '5e97b23b49ccf626cb5dff6d',
    'formioSubmittedTime': '2020-04-16T01:17:47.677Z',
    'hasNoPCP': True,
    'lastReportedWorkDate': '04/15/2020',
    'insuranceCarrier': 'United Healthcare',
    'kaiserMedicalRecordNumber': None,
    'pcpFieldSetIagreetosharemyinformationwithKaiser': None
}

SAMPLE_APPOINTMENT_CONTRACTOR = {
    'firstName': 'test',
    'lastName': 'test',
    'phone': '4158675309',
    'email': 'test@sfgov.org',
    'applicantWillDrive': 'yes',
    'canceled': False,
    'acuityId': 372213232,
    'appointmentDatetime': '2020-04-17T14:30:00-0700',
    'acuityCreatedTime': '2020-04-14T22:53:56-0500',
    'formioId': '5e98b4d69e74361dfbfe7fd8',
    'formioSubmittedTime': '2020-04-16T19:41:10.657Z',
    'workCity': 'San Francisco',
    'workAddress': '1231 Stevenson st',
    'homeState': 'CA',
    'homeAddress': '123 Main St',
    'pcpFieldSetIagreetosharemyinformationwithKaiser': None,
    'panelFieldsetYourethnicity': 'iDoNotWishToSay',
    'kaiserMedicalRecordNumber': None,
    'primaryHolderHealthInsurance': 'parent',
    'healthInsuranceGroupIdNumber': 'group id number',
    'healthInsuranceIdNumber': 'insurance id number',
    'primaryHolderHealthInsuranceFirstname': 'Parental',
    'workState': 'CA',
    'workZipcode': '94103',
    'employerNotListed': None,
    'primaryHolderHealthInsuranceLastname': 'unit',
    'businessNotListed': False,
    'lastReportedWorkDate': None,
    'middleName': 'k',
    'employer': 'AMR',
    'homeZipcode': '94703',
    'panelFieldsetYourdateofbirth': '01/01/1920',
    'panelFieldsetYoursexatbirth': 'f',
    'homeCity': 'Berkeley',
    'insuranceCarrier': 'Health Net',
    'hasNoPCP': None
}

def test_format_canceled_appointment():
    """Test that canceled appointments are passed to the correct key."""
    color = Color()
    resp = color.format_appointment(SAMPLE_CANCELED)
    assert resp['state'] == 'canceled'

def test_app_has_pcp():
    """Verify has_pcp field is correct if app has pcp."""
    color = Color()
    resp = color.format_appointment(SAMPLE_APPOINTMENT)
    #pylint: disable=singleton-comparison
    assert resp['has_pcp'] == True

def test_app_without_pcp():
    """Verify has_pcp field is correct if app doe not have pcp."""
    color = Color()
    resp = color.format_appointment(SAMPLE_WITHOUT_PCP)
    #pylint: disable=singleton-comparison
    assert resp['has_pcp'] == False

def test_format_appointment_pads_phones():
    """Verify that format_appointment formats phone numbers."""
    color = Color()
    resp = color.format_appointment(SAMPLE_APPOINTMENT)
    #pylint: disable=singleton-comparison
    assert resp['phone_number'] == '+14158675309'

def test_format_appointment_pads_dsws():
    """Verify format_appointment pads dsws if they are only 5 chars."""
    color = Color()
    appt = {**SAMPLE_APPOINTMENT, **{'dsw': '12345'}}
    resp = color.format_appointment(appt)
    #pylint: disable=singleton-comparison
    assert resp['external_id'] == '012345'

def test_format_appointment_formats_last_work_date():
    """Verify format_appointment formats last work date correctly."""
    color = Color()
    resp = color.format_appointment(SAMPLE_APPOINTMENT)
    #pylint: disable=singleton-comparison
    assert resp['last_reported_work_date'] == '2020-04-14'

def test_format_appointment_formats_applicant_will_drive():
    """Verify format_appointment formats last work date correctly."""
    color = Color()
    resp = color.format_appointment(SAMPLE_APPOINTMENT)
    assert resp['applicant_will_drive'] is True

    wont_drive = {**SAMPLE_APPOINTMENT, **{'applicantWillDrive': 'no'}}
    resp = color.format_appointment(wont_drive)
    assert resp['applicant_will_drive'] is False

def test_format_external_id_none():
    """Verify we can parse external_id if it's none."""
    color = Color()
    appt = {**SAMPLE_APPOINTMENT, **{'dsw': None}}
    resp = color.format_appointment(appt)
    assert 'external_id' not in resp

def test_format_sex_none():
    """Verify we can parse sex if it's none."""
    color = Color()
    appt = {**SAMPLE_APPOINTMENT, **{'sex': None}}
    resp = color.format_appointment(appt)
    assert 'sex' not in resp

def test_format_contractor_appt():
    """Test case with contractor data"""
    color = Color()
    resp = color.format_appointment(SAMPLE_APPOINTMENT_CONTRACTOR)

    expected = {
        'external_appointment_id': 372213232,
        'state': 'scheduled',
        'first_name': 'test',
        'last_name': 'test',
        'email': 'test@sfgov.org',
        'phone_number': '+14158675309',
        'appointment_datetime': '2020-04-17T14:30:00-0700',
        'applicant_will_drive': True,
        'insurance_carrier': 'Health Net',
        'has_pcp': False,
        'external_appointment_created_at': '2020-04-14T22:53:56-0500',
        'employer_name': 'AMR',
        'birthday': '1920-01-01',
        'ethnicity': 'iDoNotWishToSay',
        'sex': 'F',
        'middle_name': 'k',
        'address_line1': '123 Main St',
        'city': 'Berkeley',
        'postal_code': '94703',
        'worksite_address_line1': '1231 Stevenson st',
        'worksite_city': 'San Francisco',
        'worksite_state': 'CA',
        'worksite_zip': '94103',
        'insurance_primary_holder_first_name': 'Parental',
        'insurance_primary_holder_last_name': 'unit',
        'insurance_id': 'insurance id number',
        'insurance_group_id': 'group id number',
        'insurance_primary_holder': 'parent'
    }
    assert resp == expected

def test_format_with_county():
    """Check that county data is included if present."""
    color = Color()
    # Test without county
    resp = color.format_appointment(SAMPLE_APPOINTMENT_CONTRACTOR)

    assert 'county' not in resp

    # Test with county
    appt = {**SAMPLE_APPOINTMENT_CONTRACTOR, **{'county': 'Alameda County'}}
    resp = color.format_appointment(appt)

    assert resp['county'] == 'Alameda County'

def test_filters_out_empty_strings():
    """Check that we exclude empty strings if present."""
    color = Color()

    # Test with county
    appt = {**SAMPLE_APPOINTMENT_CONTRACTOR, **{'middleName': ''}}
    resp = color.format_appointment(appt)

    assert 'middle_name' not in resp
