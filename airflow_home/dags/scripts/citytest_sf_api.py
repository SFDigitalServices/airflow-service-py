# pylint: disable=fixme
"""CityTest SF send appts to Color scripts"""
import os
import sentry_sdk

from modules.formio import Formio
from modules.acuity import Acuity
from modules.citytest_sf_appointments import CityTestSFAppointments
from modules.color import Color

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
        'citytest_sf.appointments.pull_from_acuity found appointment: {}'.format(
            bool(parsed_appointment)
        ),
        'info'
    )
    # FIXME: We'll filter out test appointments -> how to exit airflow early?
    if (parsed_appointment['firstName'].lower() == 'test') and (
            os.environ['FILTER_TEST_APPTS'].lower() == 'true'
        ):
        dsw = None
        sentry_sdk.capture_message(
            'citytest_sf_api.appointments.pull_from_acuity: Test appt found, returning None',
            'warning'
        )
        # TODO: Exit airflow in a way that shows it's a success and avoids retries?
    else:
        dsw = parsed_appointment['dsw']

    # Save data
    task_instance = context['task_instance']
    task_instance.xcom_push(key='dsw', value=dsw)
    task_instance.xcom_push(key='parsed_appointment', value=parsed_appointment)

    sentry_sdk.capture_message('citytest_sf_api.appointments.pull_from_acuity.end', 'info')
    return bool(parsed_appointment)

def merge_with_formio(**context):
    """Get form.io responses for provided dsws, merge data together."""
    sentry_sdk.capture_message('citytest_sf_api.appointments.merge_with_formio.start', 'info')

    dsw = context['task_instance'].xcom_pull(
        task_ids='pull_from_acuity', key='dsw')

    if not dsw:
        print('no dsw')
        sentry_sdk.capture_message(
            'citytest_sf_api.appointments.merge_with_formio skipping due to missing dsw',
            'warning'
        )
        return True

    parsed_appointment = context['task_instance'].xcom_pull(
        task_ids='pull_from_acuity', key='parsed_appointment')

    # DSW is not a unique ID so we may get multiple responses per DSW.
    # We just take the first one we get back for now.
    # TODO: Filter on form.io submission id or token instead.
    formio_submissions = Formio.get_formio_submissions(dsw_ids=[dsw])

    parsed_formio_response = (
        CityTestSFAppointments.parse_formio_response(formio_submissions[0])[1]
        if len(formio_submissions) > 0 else {}
    )

    # Merge them together
    final_appointment = {**parsed_appointment, **parsed_formio_response}

    context['task_instance'].xcom_push(key='final_appointment', value=final_appointment)
    sentry_sdk.capture_message('citytest_sf_api.appointments.merge_with_formio.end', 'info')

    return bool(final_appointment)

def send_to_color_api(**context):
    """Send data to Color's API."""
    sentry_sdk.capture_message('citytest_sf_api.appointments.send_to_color_api.start', 'info')

    appointment = context['task_instance'].xcom_pull(
        task_ids='merge_with_formio', key='final_appointment')

    if not appointment:
        print('no appointment')
        sentry_sdk.capture_message(
            'citytest_sf_api.appointments.send_to_color_api no appointment found', 'warning')
        return True

    color = Color()
    formatted = color.format_appointment(appointment)
    success = Color.patch_appointment(formatted)
    sentry_sdk.capture_message('citytest_sf_api.appointments.send_to_color_api.end', 'info')

    return success
