"""
PTS CSV Export DAG
"""
from datetime import timedelta

import airflow
from airflow import DAG
#from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from scripts.pts_email_csv_export import trigger_export

# pylint: disable=invalid-name
default_args = {
    'owner': 'Airflow',
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
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
    'pts_email_csv_export',
    default_args=default_args,
    description='PTS Email CSV Export',
    schedule_interval='15 8 * * *',
    max_active_runs=1,
    catchup=False
)

t1 = PythonOperator(
    task_id='trigger_export',
    provide_context=True,
    python_callable=trigger_export,
    dag=dag,
)

# pylint: disable=pointless-statement
t1
