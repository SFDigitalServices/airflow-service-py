# pylint: disable=duplicate-code
"""Test functions from Color module."""
from modules.color import Color

SAMPLE_APPOINTMENT = {
    'firstName': 'test',
    'lastName': 'test',
    'phone': '9783020023',
    'email': 'andrea.egan@sfgov.org',
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
    'phone': '9783020023',
    'email': 'andrea.egan@sfgov.org',
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
