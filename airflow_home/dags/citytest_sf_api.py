"""
CityTestSF API connection between form.io, acuity, and Color
"""
from datetime import timedelta
import airflow
from airflow import DAG
#from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from scripts.citytest_sf_api import (
    get_county,
    pull_from_acuity,
    merge_with_formio,
    send_to_color_api
)

# pylint: disable=invalid-name
default_args = {
    'owner': 'Airflow',
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(1, hour=23), #?
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'trigger_rule': u'all_success'
}

dag = DAG(
    'citytest_sf_api',
    default_args=default_args,
    description='CityTestSF appointment api integration DAG',
    schedule_interval=None
)

t1 = PythonOperator(
    task_id='pull_from_acuity',
    provide_context=True,
    python_callable=pull_from_acuity,
    dag=dag,
)

t2 = PythonOperator(
    task_id='merge_with_formio',
    provide_context=True,
    python_callable=merge_with_formio,
    dag=dag,
)


t3 = PythonOperator(
    task_id='get_county',
    provide_context=True,
    python_callable=get_county,
    dag=dag,
)

t4 = PythonOperator(
    task_id='send_to_color_api',
    provide_context=True,
    python_callable=send_to_color_api,
    dag=dag,
)

# pylint: disable=pointless-statement
t1 >> t2 >> t3 >> t4
