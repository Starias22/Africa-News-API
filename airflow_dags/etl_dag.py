"""This is the module for news production DAG"""
import sys
from pathlib import Path
from datetime import timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
# Add 'src' directory to the Python path
src_path = Path(__file__).resolve().parents[2]
sys.path.append(str(src_path))
from src.config.config import SRC_PATH
from src.etl.transform.transform import transform
#a=5
#from src.etl.load import load

import pendulum
# Add 'src' directory to the Python path
#src_path = Path(__file__).resolve().parents[2]
#sys.path.append(str(src_path))

#from src.etl.extract.scrapers import beninwebtv_scraper, jeuneafrique_scaper, africa_confidential_scraper
#from src.etl.extract.external_apis import google_news_fetcher, newsapi_fetcher




#from config.config import SRC_PATH,START_HOUR,START_DAYS_AGO,ADMIN_EMAIL
#from src.airflow_email import success_email,failure_email

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    #'start_date': pendulum.today('UTC').subtract(days=START_DAYS_AGO).replace(hour=START_HOUR),
    'start_date': pendulum.today('UTC'),
    'email_on_failure': True,
    'email_on_success': True,
    'email_on_retry': True,
    'retries': 3,
    'retry_delay': timedelta(minutes=15),
    #'email':ADMIN_EMAIL
}


dag = DAG(
    'news_etl_dag',
    default_args=default_args,
    description='An hourly workflow for fetching news articles from multiples sources, transforming news and loading them into a POstgreSQL database',
    schedule=timedelta(days=1),
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
transform_task = PythonOperator(
   task_id='transform',
    python_callable=transform,
    dag=dag,
)

"""load_task = PythonOperator(
   task_id='transform',
    python_callable=load,
    dag=dag,
)"""

extract_task >> transform_task 
#>> load_task