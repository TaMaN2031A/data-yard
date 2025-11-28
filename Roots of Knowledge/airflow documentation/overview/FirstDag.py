from datetime import datetime

from airflow.sdk import DAG, task
from airflow.providers.standard.operators.bash import BashOperator

with DAG(dag_id='demo', start_date=datetime(2021, 1, 1), schedule="0 0 * * *") as dag:
    hello = BashOperator(task_id='hello', bash_command='echo hello')

    @task
    def airflow():
        print("hello")

    hello >> airflow()