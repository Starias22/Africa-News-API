"""This is the module for news production DAG"""
import sys
from pathlib import Path
from datetime import timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

# Add 'src' directory to the Python path
src_path = Path(__file__).resolve().parents[2]
sys.path.append(str(src_path))
from src.config.config import SRC_PATH, SPARK_CONNECTION_ID

from src.etl.load.load import load

import pendulum

#from config.config import SRC_PATH,START_HOUR,START_DAYS_AGO,ADMIN_EMAIL
#from src.airflow_email import success_email,failure_email

START_DAYS_AGO = 1
START_HOUR = 19
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': pendulum.today('UTC').subtract(days=START_DAYS_AGO).replace(hour=START_HOUR),
    'email_on_failure': True,
    'email_on_success': True,
    'email_on_retry': True,
    'retries': 3,
    'retry_delay': timedelta(minutes=10),
    #'email':ADMIN_EMAIL
}


dag = DAG(
    'etl_dag',
    default_args=default_args,
    description='An hourly workflow for fetching news articles from multiples sources, transforming news and loading them into a POstgreSQL database',
    schedule=timedelta(hours=1),
    catchup = False,
)

#   & python3 {SRC_PATH}/etl/extract/external_apis/newsapi_fetcher.py
extract_task = BashOperator(
    task_id='extract',
    bash_command=f'python3 {SRC_PATH}/etl/extract/scrapers/beninwebtv_scraper.py  & python3 {SRC_PATH}/etl/extract/scrapers/jeuneafrique_scraper.py & python3  {SRC_PATH}/etl/extract/scrapers/africa_confidential_scraper.py & python3 {SRC_PATH}/etl/extract/external_apis/google_news_fetcher.py',
    dag=dag,
    #on_success_callback = success_email,
    #on_failure_callback = failure_email,
)

transform_task = SparkSubmitOperator(
    task_id='transform',
    conn_id=SPARK_CONNECTION_ID,
    application=f'{SRC_PATH}/etl/transform/transform.py',  
    dag=dag,
    deploy_mode="client",
)


load_task = PythonOperator(
   task_id='load',
    python_callable=load,
    dag=dag,
)

extract_task >> transform_task >> load_task