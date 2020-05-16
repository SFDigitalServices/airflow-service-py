""" PTS Email CSV Export script """
import os
import requests
import sentry_sdk

def trigger_export(**_context):
    """ Trigger the export process in PTS dispatcher """
    sentry_sdk.capture_message('pts.csv_export.trigger.init', 'info')

    export_url = os.environ.get('PTS_DISPATCH_EXPORT_URL')
    export_key = os.environ.get('PTS_DISPATCH_KEY')
    response = requests.get(url=export_url, headers={"ACCESS_KEY":export_key})

    response.raise_for_status()

    with sentry_sdk.configure_scope() as scope:
        scope.set_extra('response', response.json())

    sentry_sdk.capture_message('pts.csv_export.trigger', 'info')
    return response.json()
