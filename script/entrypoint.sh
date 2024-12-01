#!/bin/bash

set -e

# Install the required libraries
if [ -e "/opt/airflow/requirements.txt" ]; then
    $(command -v pip) install --user -r /opt/airflow/requirements.txt
fi

# Initialize the Airflow database
if [ ! -f "/opt/airflow/airflow.db" ]; then
    airflow db init && \
    airflow users create \
    --username admin \
    --firstname admin \
    --lastname admin \
    --role Admin \
    --email admin@v01d.com \
    --password admin
fi

# Upgrade Airflow database schema
$(command -v airflow) db upgrade

# Launch Airflow webserver
exec airflow webserver