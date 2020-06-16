# SFDS airflow-service-py [![CircleCI](https://badgen.net/circleci/github/SFDigitalServices/airflow-service-py/main)](https://circleci.com/gh/SFDigitalServices/airflow-service-py) [![Coverage Status](https://coveralls.io/repos/github/SFDigitalServices/airflow-service-py/badge.svg?branch=main)](https://coveralls.io/github/SFDigitalServices/airflow-service-py?branch=main)
SFDS Airflow Service (Python)

## Requirement
* Python3 
([Mac OS X](https://docs.python-guide.org/starting/install3/osx/) / [Windows](https://www.stuartellis.name/articles/python-development-windows/))
* Pipenv & Virtual Environments ([virtualenv](https://docs.python-guide.org/dev/virtualenvs/#virtualenvironments-ref) / [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/))
* Postgres ([Mac OS X](https://wiki.postgresql.org/wiki/Homebrew))

## Get started

Cloning this repository 
> git clone https://github.com/SFDigitalServices/airflow-service-py.git my-airflow-service

Go to project directory
> $ cd my-airflow-service

Setup Environmental variables (and update as needed)
> $ cp .env.example .env

Install Pipenv (if needed)
> $ pip install --user pipenv

Install included packages
> $ pipenv install

Create Airflow database
> psql postgres  
> postgres=# CREATE DATABASE airflow

Initialize the database
> $ pipenv run airflow initdb

Create a user
> $ pipenv run airflow create_user --role=Admin --username=admin --email=admin@localhost --firstname=admin --lastname=user

Start the web server, default port is 8080
> $ pipenv run airflow webserver -p 8080

Start the scheduler
> $ pipenv run airflow scheduler

Open with cURL or web browser
> $ curl http://localhost:8080/

### Airflow How-to Guides
Quick Start: https://airflow.readthedocs.io/en/stable/start.html

Securing Connection: https://airflow.readthedocs.io/en/stable/howto/secure-connections.html

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


## Branch information

### main
Vanilla branch. This branch ontains bare minimum to get started on a new airflow instance.

### tutorial
Tutorial branch. This branch contains examples and tutorials to help get familiar with airflow.

### sfds
SFDS branch. This branch contains DAGs relevant to SFDS.
