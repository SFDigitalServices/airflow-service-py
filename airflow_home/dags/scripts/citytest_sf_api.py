# pylint: disable=fixme
# pylint: disable=trailing-newlines
"""CityTest SF send appts to Color scripts"""
import os
import sentry_sdk

from modules.formio import Formio
from modules.acuity import Acuity
from modules.citytest_sf_appointments import CityTestSFAppointments
from modules.color import Color
from modules.google_maps import GoogleMaps

def pull_from_acuity(**context):
    """Pull appointments from acuity."""
    acuity_id = context['dag_run'].conf.get('acuity_id', None)

    sentry_sdk.capture_message(
        'citytest_sf_api.appointments.pull_from_acuity.start for appointment {}'.format(acuity_id),
        'info'
    )

    # Get Acuity appointments and parse
    appt = Acuity.get_appointment(acuity_id)
    parsed_appointment = CityTestSFAppointments.parse_appointment(appt)

    sentry_sdk.capture_message(
        """
        citytest_sf.appointments.pull_from_acuity found appointment with id {acuity_id},
        formio_id {formio_id}
        """.format(
            acuity_id=acuity_id,
            formio_id=parsed_appointment['formioId']
        ),
        'info'
    )

    if not parsed_appointment['formioId'] and parsed_appointment['email']:
        parsed_appointment['formioId'] = CityTestSFAppointments.get_formio_id_by_email(
            parsed_appointment['email'])

        sentry_sdk.capture_message(
            # pylint: disable=line-too-long
            """
            citytest_sf.appointments.pull_from_acuity attempted to find formio_id with id {acuity_id},formio_id {formio_id}
            """.format(
                acuity_id=acuity_id,
                formio_id=parsed_appointment['formioId']
            ),
            'info'
        )

    # Save data
    task_instance = context['task_instance']
    task_instance.xcom_push(key='formio_id', value=parsed_appointment['formioId'])
    task_instance.xcom_push(key='parsed_appointment', value=parsed_appointment)

    sentry_sdk.capture_message('citytest_sf_api.appointments.pull_from_acuity.end', 'info')
    return bool(parsed_appointment)

def merge_with_formio(**context):
    """Get form.io responses for provided formio id, merge data together."""
    sentry_sdk.capture_message('citytest_sf_api.appointments.merge_with_formio.start', 'info')

    formio_id = context['task_instance'].xcom_pull(
        task_ids='pull_from_acuity', key='formio_id')

    parsed_appointment = context['task_instance'].xcom_pull(
        task_ids='pull_from_acuity', key='parsed_appointment')

    if formio_id:
        print('formio id found', formio_id)
        formio_submission = Formio.get_formio_submission_by_id(formio_id)
    else:
        raise Exception(
            """
            citytest_sf_api.appointments.send_to_color_api no appointment found. acuity id: {}
            """.format(context['dag_run'].conf.get('acuity_id', None))
        )

    parsed_formio_response = (
        CityTestSFAppointments.parse_formio_response(formio_submission)
    )

    # Merge them together
    final_appointment = {**parsed_appointment, **parsed_formio_response}

    context['task_instance'].xcom_push(key='final_appointment', value=final_appointment)
    sentry_sdk.capture_message('citytest_sf_api.appointments.merge_with_formio.end', 'info')

    return bool(final_appointment)

#pylint: disable=inconsistent-return-statements
def get_county(**context):
    """Add county data to appointment."""
    appointment = context['task_instance'].xcom_pull(
        task_ids='merge_with_formio', key='final_appointment')

    try:
        city = appointment.get('homeCity', None)
        state = appointment.get('homeState', None)
        print('city and state', city, state)
        if city and state:
            geocoded = GoogleMaps.geocode(city=city, state=state)
            county = GoogleMaps.get_county_from_geocode(geocoded)
            appointment['county'] = county
    #pylint: disable=broad-except
    except Exception as exp:
        context['task_instance'].xcom_push(key='appointment_with_county', value=appointment)
        sentry_sdk.capture_message(
            """
            citytest_sf_api.appointments.get_county error getting county.
            acuity id: {id}, error: {error}
            """.format(id=context['dag_run'].conf.get('acuity_id', None), error=exp),
            'error'
        )
        return True

    context['task_instance'].xcom_push(key='appointment_with_county', value=appointment)

    return True


def send_to_color_api(**context):
    """Send data to Color's API."""
    sentry_sdk.capture_message('citytest_sf_api.appointments.send_to_color_api.start', 'info')

    appointment = context['task_instance'].xcom_pull(
        task_ids='get_county', key='appointment_with_county')

    if (appointment['firstName'].lower() == 'test') and (
            os.environ['FILTER_TEST_APPTS'].lower() == 'true'
        ):
        sentry_sdk.capture_message(
            'citytest_sf_api.appointments.pull_from_acuity: Test appt found, returning True',
            'warning'
        )
        return True

    if not appointment:
        print('no appointment')
        raise Exception(
            """
            citytest_sf_api.appointments.send_to_color_api no appointment found. acuity id: {}
            """.format(context['dag_run'].conf.get('acuity_id', None))
        )

    color = Color()
    formatted = color.format_appointment(appointment)
    try:
        response = Color.patch_appointment(formatted)
        response.raise_for_status()
    #pylint: disable=broad-except
    except Exception:
        sentry_sdk.capture_message(
            """
            citytest_sf_api.send_to_color_api error.
            acuity id: {id}, status code: {status_code} error: {error}
            """.format(
                id=context['dag_run'].conf.get('acuity_id', None),
                status_code=response.status,
                error=response.text
            ),
            'error'
        )
        raise

    sentry_sdk.capture_message('citytest_sf_api.appointments.send_to_color_api.end', 'info')
    return response.ok


