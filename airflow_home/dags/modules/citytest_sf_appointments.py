"""Functions related to business logic around CityTestSF appts."""
import collections

import sentry_sdk

from modules.core import Core

class CityTestSFAppointments(Core):
    """Functions related to business logic around CityTestSF appts."""
    @staticmethod
    def parse_appointment(appointment):
        """Retrieve fields needed from acuity appt."""
        dsw_field_id = 7514073
        form_id = 1368026
        driving_field_id = 7543629
        top_level_fields = [
            'firstName',
            'lastName',
            'phone',
            'email',
            'datetime',
            'datetimeCreated',
            'id'
        ]
        # Filter to only keys that we want
        parsed = dict((k, appointment[k]) for k in top_level_fields if k in appointment)

        # Get DSW and driving status from form
        # Looks like next is the most performant way to do this search
        # https://stackoverflow.com/questions/8653516/python-list-of-dictionaries-search
        form = next(
            (item.get('values') for item in appointment['forms'] if item['id'] == form_id),
            []
        )
        dsw = next((item.get('value') for item in form if item['fieldID'] == dsw_field_id), None)
        parsed['dsw'] = dsw if dsw else None
        parsed['applicantWillDrive'] = next(
            (item.get('value') for item in form if item['fieldID'] == driving_field_id),
            None
        )

        # Rename id and datetime
        parsed['acuityId'] = parsed.pop('id')
        parsed['appointmentDatetime'] = parsed.pop('datetime')
        parsed['acuityCreatedTime'] = parsed.pop('datetimeCreated')

        return parsed

    @staticmethod
    def parse_formio_response(response):
        """Get desired fields from formio, return dsw and values."""
        data = response['data']
        dsw = data['dsw']

        parsed = {
            'formioId': response['_id'],
            'formioSubmittedTime': response['created'],
            'hasNoPCP': data.get('hasPCP', None),
            'lastReportedWorkDate': data.get('lastReportedWorkDate', None),
            'insuranceCarrier': data.get('insuranceCarrier', None),
            'kaiserMedicalRecordNumber': data.get('kaiserMedicalRecordNumber', None),
            'pcpFieldSetIagreetosharemyinformationwithKaiser': data.get(
                'pcpFieldSetIagreetosharemyinformationwithKaiser', None
            )
        }
        if 'pcp' in data:
            parsed.update(data['pcp'])

        return (dsw, parsed)

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
