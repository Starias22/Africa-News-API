"""This module defines configuration variables"""
import json
import os
from pathlib import Path

START_HOUR=2
START_DAYS_AGO=0

# Load configurations from config.json
# Use absolute path to ensure we find the file
abs_filepath = os.path.join(os.path.dirname(__file__), 'secret.json')
with open(abs_filepath, 'r', encoding='utf-8') as file:
    config=json.load(file)

# Assign configurations to variables
NEWSAPI_KEYS = [
    config.get("newsapi_key", ""),
    config.get("newsapi_key2", ""),
    config.get("newsapi_key3", ""),
    config.get("newsapi_key4", ""),
    config.get("newsapi_key5", "")
]
#NEWSDATAAPI_KEY = config.get("newsdataapi_key", "")
LANGUAGES = ["en","fr","es"]
PAGE_SIZE = 100
HOURS_PERIOD = 25
QUERY = ["technology","finance","health","economy","war","business",
    "biology","science","politics","family","ecology","coronavirus","Gaza",
    "Israel","Palsestine","Ukraine","Benin","Niger","Morocco","sports","Trump",
    "Biden","education","crime","justice","religion","travel","weddings","styles","nation"
  ]
PAGE = 1 # Example default value


SPARK_VERSION = "3.5.1"
SENDER_ADDRESS=config.get("sender_address")
PASSWORD=config.get("password")
ADMIN_EMAIL=config.get("admin_email")
MONGO_DB_NAME="news_recommendation_db"

#os.environ.pop('MONGO_DB_URI', None)
MONGO_DB_URI=os.getenv("MONGO_DB_URI","mongodb://localhost:27017/")
#print(888888888888888888888)
print(MONGO_DB_URI)
LOCALHOST="localhost"
REDIS_HOST=os.getenv("REDIS_HOST",LOCALHOST)
TIME_OUT_MS=1000
GROUP_TIME_OUT_MS=5000
DISLIKED=-1
SEEN=0
LIKED=1


# Paths
PROJECT_ROOT = Path(__file__).parent.parent.resolve()

# Resolve the path to the 'src' directory
path = PROJECT_ROOT
print(path)
#print("222222222222222222")
print("Project root", PROJECT_ROOT)

SRC_PATH=str(os.getenv("SRC_PATH",path))


print("SRC path is", SRC_PATH)

NEWS_COUNTRIES_PATH=str(os.getenv("NEWS_COUNTRIES_PATH",PROJECT_ROOT/"news_countries"))

print("News countries path is", NEWS_COUNTRIES_PATH)

ETL_LOGS_PATH=os.getenv("ETL_LOGS_PATH",str(PROJECT_ROOT/'logs/etl_logs/'))
print("ETL logs path", ETL_LOGS_PATH)

STAGING_AREA_PATH=os.getenv("STAGING_AREA_PATH",str(PROJECT_ROOT/'staging_area/'))
#print("11111111111111111111111111")
print("Staging area path", STAGING_AREA_PATH)




SPARK_KAFKA_PACKAGES="org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,\
org.apache.spark:spark-token-provider-kafka-0-10_2.12:3.5.1"

SPARK_CONNECTION_ID="spark-connection"