"""
OOC Proposed cannabis retail locations DAG
"""
from datetime import timedelta

import airflow
from airflow import DAG
#from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from scripts.ooc_proposed_retail import pull_from_screendoor, push_to_datasf

# pylint: disable=invalid-name
default_args = {
    'owner': 'Airflow',
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(2),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
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
    'ooc_proposed_retail',
    default_args=default_args,
    description='OOC Proposed Retail DAG',
    schedule_interval='0 7 * * *',
)

t1 = PythonOperator(
    task_id='pull_from_screendoor',
    provide_context=True,
    python_callable=pull_from_screendoor,
    dag=dag,
)

t2 = PythonOperator(
    task_id='push_to_datasf',
    provide_context=True,
    python_callable=push_to_datasf,
    dag=dag,
)

# pylint: disable=pointless-statement
t1 >> t2
