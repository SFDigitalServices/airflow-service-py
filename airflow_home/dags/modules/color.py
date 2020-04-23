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
        'state': 'canceled',
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
        # Contractor
        'employer_name': 'employer',
        'birthday': 'panelFieldsetYourdateofbirth',
        'ethnicity': 'panelFieldsetYourethnicity',
        'sex': 'panelFieldsetYoursexatbirth',
        'middle_name': 'middleName',
        'address_line1': 'homeAddress',
        'city': 'homeCity',
        'county': 'county',
        # 'state': 'homeState', # Not sending now due to conflict with canceled state field
        'postal_code': 'homeZipcode',
        'worksite_address_line1': 'workAddress',
        'worksite_city': 'workCity',
        'worksite_state': 'workState',
        'worksite_zip': 'workZipcode',
        'insurance_primary_holder_first_name': 'primaryHolderHealthInsuranceFirstname',
        'insurance_primary_holder_last_name': 'primaryHolderHealthInsuranceLastname',
        'insurance_id': 'healthInsuranceIdNumber',
        'insurance_group_id': 'healthInsuranceGroupIdNumber',
        'insurance_primary_holder': 'primaryHolderHealthInsurance',
    }

    EMBARCADERO_SITE_NAME = 'Embarcadero'
    SOMA_SITE_NAME = 'SOMA'

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
        if not date_string:
            return None
        d_t = datetime.strptime(date_string, '%m/%d/%Y')
        return d_t.strftime('%Y-%m-%d')

    def get_collection_site(self, appointment):
        """Return collection site based on calendar id."""
        cal_id = str(appointment.get('calendarID', None))
        if cal_id == os.environ.get('EMBARCADERO_CALENDAR_ID'):
            return self.EMBARCADERO_SITE_NAME
        if cal_id == os.environ.get('SOMA_CALENDAR_ID'):
            return self.SOMA_SITE_NAME
        # Raise sentry warning.
        # Default to Embarcadero.
        print('Warning: Defaulting to Embarcadero', cal_id)
        return self.EMBARCADERO_SITE_NAME



    def format_appointment(self, appointment):
        """Take our parsed appointment and ensure it has correct keys and values for Color."""
        formatted = {
            key: appointment[value] for (key, value)
            in self.field_map.items() if value in appointment
        }

        # Format contractor fields if present
        # TODO: do this with less copy pasta
        if formatted.get('sex', None):
            formatted['sex'] = formatted['sex'].upper()
        if 'birthday' in formatted:
            formatted['birthday'] = Color.isoformat_date(formatted['birthday'])
        if formatted.get('external_id', None):
            formatted['external_id'] = Color.format_dsw(formatted['external_id'])
        if 'phone_number' in formatted:
            formatted['phone_number'] = Color.format_phone(formatted['phone_number'])

        # Do some extra formatting to prep for sending to the Color API.
        formatted['last_reported_work_date'] = Color.isoformat_date(
            formatted['last_reported_work_date']
        )
        formatted['applicant_will_drive'] = Color.yes_no_to_bool(formatted['applicant_will_drive'])
        formatted['state'] = 'canceled' if formatted['state'] else 'scheduled'
        # flipping the logic from has no pcp to has pcp
        # pylint: disable=singleton-comparison
        formatted['has_pcp'] = formatted['has_pcp'] == False

        # Hardcode worksite state because we do not ask in the form.
        formatted['worksite_state'] = 'CA'

        # Get the collection site
        formatted['collection_site'] = self.get_collection_site(appointment)

        # Strip out null values after parsing
        formatted = {k: v for k, v in formatted.items() if v not in (None, '')}

        return formatted

    @staticmethod
    def patch_appointment(
            appointment,
            api_endpoint=os.environ.get('COLOR_API_ENDPOINT'),
            password=os.environ.get('COLOR_API_PASSWORD'),
            user='',
        ):
        """Send appointment to Color via patch request."""

        response = requests.patch(
            api_endpoint,
            auth=HTTPBasicAuth(user, password),
            json=appointment
        )


        return response
