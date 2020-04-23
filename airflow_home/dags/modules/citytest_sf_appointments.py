# pylint: disable=fixme
"""Functions related to business logic around CityTestSF appts."""
import collections

import sentry_sdk

from modules.core import Core
from modules.acuity import Acuity

class CityTestSFAppointments(Core):
    """Functions related to business logic around CityTestSF appts."""
    @staticmethod
    def parse_appointment(appointment, extra_fields=None):
        """Retrieve fields needed from acuity appt."""
        user_entered_form_id = 1368026
        driving_field_id = 7543629
        internal_use_form_id = 1369277
        formio_id_field_id = 7570420
        top_level_fields = [
            'firstName',
            'lastName',
            'phone',
            'email',
            'datetime',
            'datetimeCreated',
            'id',
            'canceled'
        ]
        if extra_fields:
            top_level_fields += extra_fields
        # Filter to only keys that we want
        parsed = dict((k, appointment[k]) for k in top_level_fields if k in appointment)

        # Get DSW and driving status from form
        user_entered_form = Acuity.get_form_values(appointment, user_entered_form_id)
        parsed['applicantWillDrive'] = Acuity.get_form_value(user_entered_form, driving_field_id)

        # Get the formioId
        machine_entered_form = Acuity.get_form_values(appointment, internal_use_form_id)
        parsed['formioId'] = Acuity.get_form_value(machine_entered_form, formio_id_field_id)


        # Rename id and datetime
        parsed['acuityId'] = parsed.pop('id')
        parsed['appointmentDatetime'] = parsed.pop('datetime')
        parsed['acuityCreatedTime'] = parsed.pop('datetimeCreated')

        return parsed

    @staticmethod
    def parse_formio_response(response):
        """Get desired fields from formio, return dsw and values."""
        data = response['data']

        data_fields = {
            'dsw',
            'hasPCP',
            'lastReportedWorkDate',
            'insuranceCarrier',
            'kaiserMedicalRecordNumber',
            'pcpFieldSetIagreetosharemyinformationwithKaiser',
            'employerNotListed',
            'employer',
            'businessNotListed',
            'panelFieldsetYourdateofbirth',
            'panelFieldsetYourethnicity',
            'panelFieldsetYoursexatbirth',
            'middleName',
            'homeAddress',
            'homeCity',
            'homeState',
            'homeZipcode',
            'workAddress',
            'workCity',
            'workState',
            'workZipcode',
            'primaryHolderHealthInsuranceFirstname',
            'primaryHolderHealthInsuranceLastname',
            'healthInsuranceIdNumber',
            'healthInsuranceGroupIdNumber',
            'primaryHolderHealthInsurance',
        }

        parsed = {
            'formioId': response['_id'],
            'formioSubmittedTime': response['created'],
        }

        for field in data_fields:
            parsed[field] = data.get(field, None)

        # TODO: fix this confusing logic.
        parsed['hasNoPCP'] = parsed.pop('hasPCP', None)

        # Merge unlisted employer data into employer if present
        if parsed.get('businessNotListed'):
            parsed['employer'] = parsed['employerNotListed']

        if 'pcp' in data:
            parsed.update(data['pcp'])

        return parsed

    @staticmethod
    def check_for_appt_duplicates(parsed_appts):
        """Given a list of appointments, check for DSWs that have scheduled multiple appts."""
        dsws = [appt['dsw'] for appt in parsed_appts if appt['dsw']]
        dup_dsws = {dsw:count for dsw, count in collections.Counter(dsws).items() if count > 1}
        sentry_sdk.capture_message(
            'citytest_sf_appointments.check_for_appt_duplicates found duplicate DSWs: {}'.format(
                dup_dsws
            ), 'info'
        )
        return dup_dsws

    @staticmethod
    def merge_acuity_formio(parsed_appointments, parsed_responses):
        """Merge a list of acuity appointments and a dictionary of formio appts keyed on DSW."""
        merged = []
        for appointment in parsed_appointments:
            dsw = appointment['dsw']
            formio_merge = parsed_responses.get(dsw, {}) if dsw else {}
            if not formio_merge:
                sentry_sdk.capture_message(
                    'citytest_sf_appointments.merge_acuity_formio missing form.io for dsw {}'.
                    format(dsw),
                    'warning'
                )
            merged.append({**appointment, **formio_merge})
        return merged
