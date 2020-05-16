"""
CityTestSF Appointment Report DAG
"""
from datetime import timedelta

import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from scripts.citytest_sf_appointments_report import refresh_appointment_data

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
    'citytest_sf_report_appt',
    default_args=default_args,
    description='CityTestSF Appointment Report DAG',
    schedule_interval=None,
    max_active_runs=1,
    catchup=False
)

t1 = PythonOperator(
    task_id='refresh_appointment_data',
    provide_context=True,
    python_callable=refresh_appointment_data,
    dag=dag,
)

# pylint: disable=pointless-statement
t1
