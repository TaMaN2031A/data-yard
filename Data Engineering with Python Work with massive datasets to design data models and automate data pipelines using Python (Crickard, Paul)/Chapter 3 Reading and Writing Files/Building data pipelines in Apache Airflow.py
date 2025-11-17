import datetime as dt

from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator
import pandas as pd

def csv_to_json():
    df = pd.read_csv('data.csv')
    df.to_json('dag_data.json', orient='records')

default_args = {
    'owner': 'airflow',
    'start_date': dt.datetime(2025, 11, 17),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5)
}
with DAG(
    'MyCSVDag',
    default_args=default_args,
    schedule=dt.timedelta(minutes=5),
) as dag:
    print_starting = BashOperator(
        task_id='starting',
        bash_command='echo "I am reading the csv now"'
    )
    csvtojson_task = PythonOperator(
        task_id='csvtojson',
        python_callable=csv_to_json,
    )
    print_starting >> csvtojson_task

