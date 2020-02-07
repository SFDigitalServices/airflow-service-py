""" OOC Proposed Retail script """
import os
import requests
import sentry_sdk
from modules.ooc_proposed_retail import OOCProposedRetail
from modules.datasf import DataSF

def pull_from_screendoor(**context):
    """ pull from screendoor """
    proposed_retail = OOCProposedRetail()
    sentry_sdk.capture_message('ooc.proposed_retail.pull_from_screendoor.init', 'info')

    proposed_retail.init_screendoor(
        os.environ['OOC_SD_KEY'], '1',
        os.environ['SD_HOST'], os.environ['OOC_SD_PROJECT']
    )

    permit_list = proposed_retail.get_permit_list('proposed_retail')

    data = proposed_retail.get_datasf_list_transform(permit_list)
    sentry_sdk.capture_message('ooc.proposed_retail.pull_from_screendoor', 'info')

    task_instance = context['task_instance']
    task_instance.xcom_push(key="proposed_retail_list", value=data)

    return bool(data)

def push_to_datasf(**context):
    """ push to datasf """
    data = context['task_instance'].xcom_pull(
        task_ids='pull_from_screendoor', key='proposed_retail_list')
    datasf = DataSF()
    sentry_sdk.capture_message('ooc.proposed_retail.push_to_datasf.init', 'info')

    replaced = datasf.replace('proposed_retail', data)
    sentry_sdk.capture_message('ooc.proposed_retail.push_to_datasf', 'info')

    return replaced

def notify_website(**context):
    """ notifiy ooc website new data is available """
    notified = False

    notify_url = os.environ['OOC_WEB_NOTIFY']

    if notify_url:
        response = requests.get(notify_url)
        notified = response.status_code

        task_instance = context['task_instance']
        task_instance.xcom_push(key="notify_website_response", value=response.text)

    return notified
