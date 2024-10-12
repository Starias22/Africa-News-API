#!/bin/bash

# Create the main data directory and navigate into it
mkdir data
cd data

# Create directories for checkpoints
#mkdir -p checkpoint/filtered_news/ -p checkpoint/available_news/ -p checkpoint/processed_news/

# Create directory for redis, PostgreSQL and MongoDB
mkdir redis/ postgres 

# Create directory for Airflow logs
mkdir -p logs/airflow_logs/

# Create directory for Airflow logs
mkdir -p logs/etl_logs/

mkdir staging_area/


# Navigate back to the parent directory
cd ..



# Set permissions for checkpoint directories
#chmod -R 777 data/checkpoint/{filtered_news,available_news,processed_news}/

# Set permissions for Redis, PostgresQL and MongoDB directories
chmod -R 755 data/{redis,postgres}/

# Set permissions for Airflow logs directory
chmod -R 777 data/logs/airflow_logs/

chmod -R 777 data/logs/etl_logs/
chmod -R 777 data/staging_area/