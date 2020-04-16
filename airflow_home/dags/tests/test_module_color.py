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
