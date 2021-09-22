# Importing the date wrangling
from datetime import timedelta

# Path traversal
import sys 
import os 
sys.path.insert(0,os.path.abspath(os.path.dirname(__file__)))

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

# Importing the ML pipeline parts
from get_weather_data import get_weather_data
from upload_weather_data import upload_weather_data
from clean_data_dirs import clean_data_dirs

# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email': ['elasorama@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

# Instantiates a directed acyclic graph
dag = DAG(
    'Vilnius-weather-pipeline',
    default_args=default_args,
    description='A pipeline that downloads the newest weather data for Vilnius via an API, trains and LSTM model and pushes the model to production',
    schedule_interval=timedelta(days=1),
)

## Defining each step of the DAGs
# Downloading data from OpenWeather API
download_data = PythonOperator(
    task_id='download_data',
    python_callable=get_weather_data,
    dag=dag,
)

# Cleaning the downloaded data
clean_data_dirs = PythonOperator(
    task_id='clean_data_dirs',
    python_callable=clean_data_dirs,
    dag=dag,
)

# Uploading raw data to database
upload_weather_data = PythonOperator(
    task_id='upload_weather_data',
    python_callable=upload_weather_data,
    dag=dag,
)

# The whole pipeline
download_data >> clean_data_dirs >> upload_weather_data