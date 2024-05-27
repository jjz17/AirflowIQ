from airflow import DAG
from airflow.operators.python import PythonOperator
import pandas as pd
import requests
from datetime import datetime
from dotenv import dotenv_values


env_vars = dotenv_values()

MYSQL_USER = env_vars["MYSQL_USER"]
MYSQL_PASSWORD = env_vars["MYSQL_PASSWORD"]



default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1
}

with DAG(
    'airnow_data_pipeline',
    default_args=default_args,
    description='A DAG to fetch, transform, and visualize AirNow data',
    schedule='@daily',
    # start_date=days_ago(1),
    start_date=datetime(2024, 3, 15, 1),
    tags=['airnow', 'data_pipeline'],
) as dag:

    fetch_data_task = PythonOperator(
        task_id='fetch_airnow_data',
        python_callable=fetch_airnow_data
    )

    transform_data_task = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data
    )

    plot_chart_task = PythonOperator(
        task_id='plot_chart',
        python_callable=plot_chart
    )

    fetch_data_task >> transform_data_task >> plot_chart_task