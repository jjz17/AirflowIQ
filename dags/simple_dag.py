from airflow import DAG
from airflow.operators.bash import BashOperator

from datetime import datetime, timedelta


default_args = {"owner": "jason", "retries": 5, "retry_delay": timedelta(minutes=2)}


with DAG(
    dag_id="first_dag_v4",
    default_args=default_args,
    description="First basic airflow dag",
    start_date=datetime(2024, 3, 15, 1),
    schedule_interval="@daily",
) as dag:
    task1 = BashOperator(
        task_id="first_task", bash_command="echo hello world, this is my first task!"
    )

    task2 = BashOperator(
        task_id="second_task",
        bash_command="echo this is the second task, running after task1!",
    )

    task3 = BashOperator(
        task_id="third_task",
        bash_command="echo this is the third task, running after task1!",
    )

    # task1.set_downstream(task2)
    # task1.set_downstream(task3)

    task1 >> [task2, task3]
