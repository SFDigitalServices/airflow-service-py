# pylint: disable=fixme
"""Functions and business logic related to Color's api."""
from datetime import datetime
import os
import requests
from requests.auth import HTTPBasicAuth

from modules.core import Core

class Color(Core):
    """ Integrate with Color's API """
    field_map = {
        'external_id': 'dsw',
        'external_appointment_id': 'acuityId',
        'status': 'canceled',
        'first_name': 'firstName',
        'last_name': 'lastName',
        'email': 'email',
        'phone_number': 'phone',
        'appointment_datetime': 'appointmentDatetime',
        'applicant_will_drive': 'applicantWillDrive',
        'last_reported_work_date': 'lastReportedWorkDate',
        'insurance_carrier': 'insuranceCarrier',
        'has_pcp': 'hasNoPCP',
        'pcp_first_name': 'pcpFirstName',
        'pcp_last_name': 'pcpLastName',
        'pcp_practice': 'pcpPractice',
        'pcp_city': 'pcpCity',
        'pcp_state': 'pcpState',
        #pylint: disable=line-too-long
        'authorized_color': 'iAuthorizeColorToShareMyInformationAndTestResultsWithThePrimaryCarePhysicianIHaveIdentifiedOnThisFormForTreatmentAndCarePurposes',
        'external_appointment_created_at': 'acuityCreatedTime',
        #pylint: disable=line-too-long
        'agree_to_share_information_with_kaiser': 'pcpFieldSetIagreetosharemyinformationwithKaiser',
        'kaiser_medical_record_number': 'kaiserMedicalRecordNumber',
    }

    # TODO: format phone number correctly
    @staticmethod
    def format_phone(phone):
        """Add country code to phone numbers we get from acuity."""
        return '+1{}'.format(phone)

    @staticmethod
    def format_dsw(dsw):
        """0-pad DSWs if they are less than 6 characters."""
        return dsw.rjust(6, '0')

    # TODO: will passing null cause an issue for color?
    @staticmethod
    def yes_no_to_bool(answer):
        """Convert yes/no answers to bools."""
        if answer == 'yes':
            return True
        if answer == 'no':
            return False
        return None

    @staticmethod
    def isoformat_date(date_string):
        """Convert from mm/dd/yyyy to yyyy-mm-dd."""
        d_t = datetime.strptime(date_string, '%m/%d/%Y')
        return d_t.strftime('%Y-%m-%d')

    def format_appointment(self, appointment):
        """Take our parsed appointment and ensure it has correct keys and values for Color."""
        formatted = {
            key: appointment[value] for (key, value)
            in self.field_map.items() if value in appointment
        }

        # Do some extra formatting to prep for sending to the Color API.
        formatted['external_id'] = Color.format_dsw(formatted['external_id'])
        formatted['phone_number'] = Color.format_phone(formatted['phone_number'])
        formatted['last_reported_work_date'] = Color.isoformat_date(
            formatted['last_reported_work_date']
        )
        formatted['applicant_will_drive'] = Color.yes_no_to_bool(formatted['applicant_will_drive'])
        formatted['status'] = 'canceled' if formatted['status'] else 'scheduled'
        # flipping the logic from has no pcp to has pcp
        formatted['has_pcp'] = not formatted['has_pcp']

        # Strip out null values after parsing
        formatted = {k: v for k, v in formatted.items() if v is not None}

        # maybe just add a step to remove nulls?
        return formatted

    @staticmethod
    def patch_appointment(
            appointment,
            api_endpoint=os.environ.get('COLOR_API_ENDPOINT'),
            password=os.environ.get('COLOR_API_PASSWORD'),
            user=os.environ.get('COLOR_API_USER'),
        ):
        """Send appointment to Color via patch request."""

        response = requests.patch(
            api_endpoint,
            auth=HTTPBasicAuth(user, password),
            json=appointment
        )
        print('response.status', response.status_code)
        response.raise_for_status()

        return response.ok
