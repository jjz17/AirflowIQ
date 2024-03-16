from airflow import DAG
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
import json
import pandas as pd
import numpy as np

# Define the DAG configuration
default_args = {
    "owner": "jason_zhang",
    "start_date": days_ago(1),
    "schedule_interval": "0 * * * *",  # Run hourly (Cronjob scheduling)
}

dag = DAG(
    "air_quality_pipeline",
    default_args=default_args,
    description="Air Quality Data Pipeline",
    catchup=False,  # Set to False to skip historical runs on first execution
    tags=["data-pipeline"]
)

# Define the OpenAQ API endpoint for real-time air quality data
url_v1 = "https://api.openaq.org/v1/latest/550?limit=100&page=1&offset=0&sort=asc"
headers = {"accept": "application/json"}

# Task to extract real-time air quality data
def extract_data():
    # Use the SimpleHttpOperator to make the API request
    response = SimpleHttpOperator(
        task_id="extract_air_quality_data",
        http_conn_id="openaq_api_conn",  # Create a connection in Airflow to store API credentials
        endpoint=url_v1,
        method="GET",
        headers=headers,
    )
    print(response)
    return json.loads(response.text)

# Task to transform the data
def transform_data(data):
    # Example data transformation: Convert JSON to a DataFrame
    df = pd.DataFrame(data["results"])
    print(df)
    # Additional transformations can be applied here
    return df

# Task to perform data analysis
def analyze_data(df):
    # Example data analysis: Calculate average air quality
    # average_air_quality = df["value"].mean()
    # return average_air_quality
    return df["location"]

# Task to trigger alerts based on analysis
def trigger_alerts(average_air_quality):
    # Example: Send an alert if air quality drops below a threshold
    if average_air_quality < 50:
        # Implement your alerting logic here
        print("Alert: Air quality is below the threshold!")

# Task to generate reports
def generate_report(df):
    # Example: Generate a simple report
    report = df.head()
    # Additional reporting logic can be applied here
    print(report)

# Define the task dependencies
data_extraction_task = PythonOperator(
    task_id="extract_data",
    python_callable=extract_data,
    dag=dag,
)

data_transformation_task = PythonOperator(
    task_id="transform_data",
    python_callable=transform_data,
    provide_context=True,
    dag=dag,
)

data_analysis_task = PythonOperator(
    task_id="analyze_data",
    python_callable=analyze_data,
    provide_context=True,
    dag=dag,
)

# alerting_task = PythonOperator(
#     task_id="trigger_alerts",
#     python_callable=trigger_alerts,
#     provide_context=True,
#     dag=dag,
# )

reporting_task = PythonOperator(
    task_id="generate_report",
    python_callable=generate_report,
    provide_context=True,
    dag=dag,
)

# Define task dependencies
# data_extraction_task >> data_transformation_task >> data_analysis_task >> alerting_task >> reporting_task
data_extraction_task >> data_transformation_task >> data_analysis_task >> reporting_task

if __name__ == "__main__":
    dag.cli()