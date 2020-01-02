# SFDS airflow-service-py [![CircleCI](https://badgen.net/circleci/github/SFDigitalServices/airflow-service-py/master)](https://circleci.com/gh/SFDigitalServices/airflow-service-py) [![Coverage Status](https://coveralls.io/repos/github/SFDigitalServices/airflow-service-py/badge.svg?branch=master)](https://coveralls.io/github/SFDigitalServices/airflow-service-py?branch=master)
SFDS Airflow Service (Python)

## Requirement
* Python3 
([Mac OS X](https://docs.python-guide.org/starting/install3/osx/) / [Windows](https://www.stuartellis.name/articles/python-development-windows/))
* Pipenv & Virtual Environments ([virtualenv](https://docs.python-guide.org/dev/virtualenvs/#virtualenvironments-ref) / [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/))

## Get started

Install Pipenv (if needed)
> $ pip install --user pipenv

Install included packages
> $ pipenv install

Initialize the database
> $ pipenv run airflow initdb

Start the web server, default port is 8080
> $ pipenv run airflow webserver -p 8080

Start the scheduler
> $ pipenv run airflow scheduler

Open with cURL or web browser
> $ curl http://localhost:8080/

## Development 

Install included packages (including development packages)
> $ pipenv install --dev

Set up git hook scripts with pre-commit
> $ pipenv run pre-commit install

Run Pytest
> $ pipenv run python -m pytest

Code coverage command with missing statement line numbers  
> $ pipenv run python -m pytest --cov=airflow_home/dags/{scripts,modules} airflow_home/dags/tests/ --cov-report term-missing


## Continuous integration
* CircleCI builds fail when trying to run coveralls.
    1. Log into coveralls.io to obtain the coverall token for your repo.
    2. Create an environment variable in CircleCI with the name COVERALLS_REPO_TOKEN and the coverall token value.
