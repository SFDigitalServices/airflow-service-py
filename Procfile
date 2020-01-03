web: export AIRFLOW__CORE__SQL_ALCHEMY_CONN=$DATABASE_URL && pipenv run airflow webserver -p $PORT
worker: export AIRFLOW__CORE__SQL_ALCHEMY_CONN=$DATABASE_URL && pipenv run airflow scheduler