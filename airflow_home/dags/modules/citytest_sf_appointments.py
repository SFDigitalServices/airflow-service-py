import collections

from modules.core import Core

class CityTestSFAppointments(Core):
    def parse_appointment(self, appointment):
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
        # Looks like next is the most performant way to do this search https://stackoverflow.com/questions/8653516/python-list-of-dictionaries-search
        form = next((item.get('values') for item in appointment['forms'] if item['id'] == form_id), [])
        dsw = next((item.get('value') for item in form if item['fieldID'] == dsw_field_id), None)
        parsed['dsw'] = dsw if dsw else None
        parsed['applicantWillDrive'] = next((item.get('value') for item in form if item['fieldID'] == driving_field_id), 'Unknown')

        # Rename id and datetime
        parsed['acuityId'] = parsed.pop('id')
        parsed['appointmentDatetime'] = parsed.pop('datetime')
        parsed['acuityCreatedTime'] = parsed.pop('datetimeCreated')


        return parsed


    def parse_formio_response(self, response):
        data = response['data']
        dsw = data['dsw']

        parsed = {
            'hasNoPCP': data.get('hasPCP', None),
            'formioSubmittedTime': response['created'],
            'lastReportedWorkDate': data.get('lastReportedWorkDate', None),
            'insuranceCarrier': data.get('insuranceCarrier', 'missing'),
            'kaiserMedicalRecordNumber': data.get('kaiserMedicalRecordNumber', None),
            'pcpFieldSetIagreetosharemyinformationwithKaiser': data.get('pcpFieldSetIagreetosharemyinformationwithKaiser', None),
            'formioId': response['_id']
        }
        if ('pcp' in data): parsed.update(data['pcp'])

        return (dsw, parsed)

    def check_for_appt_duplicates(self, parsed_appts):
        dsws = [appt['dsw'] for appt in parsed_appts if appt['dsw']]
        dup_dsws = { dsw:count for dsw, count in collections.Counter(dsws).items() if count >1 }
        print('Duplicate DSWs: ', dup_dsws)
        return dup_dsws

    def merge_acuity_formio(self, parsed_appointments, parsed_responses):
        merged = []
        for appointment in parsed_appointments:
            dsw = appointment['dsw']
            formio_merge = parsed_responses.get(dsw, {}) if dsw else {}
            if not formio_merge: print('Missing formio data for DSW:', dsw)
            merged.append({**appointment, **formio_merge})
        return merged