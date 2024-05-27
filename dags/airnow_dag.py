from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import pandas as pd
import requests
# import matplotlib.pyplot as plt
from datetime import datetime
from dotenv import dotenv_values
# import act


# env_vars = dotenv_values()
# api_key = env_vars["AIRNOW_API_KEY"]
api_key = "EAE6339B-0973-4F2E-923F-C117D76AB882"

# keys are upper bounds (inclusive) for each aqi category, and values are associated information
aqi_def_map = {50: "Good;Little to no risk",
               100: "Moderate;Acceptable, risk for those who are very sensitive to air pollution",
               150: "Unhealthy for Sensitive Groups;Risky for members of sensitive groups, general public likely not affected",
               200: "Unhealthy;Some members of general public may be affected, serious for sensitive groups",
               300: "Very Unhealthy;Increased risk for everyone",
               500: "Hazardous;Emergency conditions for everyone"}

def get_aqi_category(df):
    df_copy = df.copy(deep=True)
    category = []
    desc = []
    for j, row in df.iterrows():
        measure = row["AQI"]
        for i, pair in enumerate(aqi_def_map.items()):
            key, val = pair
            if measure <= key:
                info = val.split(";")
                category.append(info[0])
                desc.append(info[1])
                break
    df_copy["Category"] = category
    df_copy["Description"] = desc
    return df_copy


def fetch_airnow_data(**kwargs):
    # Fetch data from AirNow API
    # df = act.discovery.get_airnow_forecast(api_key, '2024-4-29', zipcode="10001", distance=100).to_dataframe()
    url = "https://www.airnowapi.org/aq/forecast/zipCode/?format=application/json&zipCode=90210&date=2024-04-28&distance=25&API_KEY=" + api_key
    response = requests.get(url)
    data = response.json()
    return pd.DataFrame(data)
    # return df

def transform_data(**kwargs):
    # Perform data transformation with Pandas
    ti = kwargs['ti']
    df = ti.xcom_pull(task_ids='fetch_airnow_data')
    
    df_agg = df[["ParameterName", "AQI"]].groupby("ParameterName").mean()

    transformed_df = get_aqi_category(df_agg)
    return transformed_df

def plot_chart(**kwargs):
    # Generate matplotlib chart
    ti = kwargs['ti']
    transformed_df = ti.xcom_pull(task_ids='transform_data')

    # plt.figure(figsize=(10, 6))
    # for area in transformed_data['ReportingArea'].unique():
    #     area_data = transformed_data[transformed_data['ReportingArea'] == area]
    #     plt.plot(area_data['DateForecast'], area_data['AQI'], label=area)
    
    # plt.title('Air Quality Index Over Time')
    # plt.xlabel('Date')
    # plt.ylabel('AQI')
    # plt.legend()
    # plt.grid(True)
    # plt.xticks(rotation=45)
    
    # # Save chart
    # plt.savefig('/path/to/save/chart.png')
    print(transformed_df)

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
