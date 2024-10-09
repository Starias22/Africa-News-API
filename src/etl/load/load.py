import csv
import psycopg2
import glob
from datetime import datetime

import os
import sys
from datetime import datetime
# Add the `src` directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from src.logs.log import Logger


# Function to retrieve primary key/foreign key from a table with multiple columns
def get_id_from_table(conn, table_name, key_column, value_columns, values):
    with conn.cursor() as cur:
        conditions = " AND ".join([f"{col} = %s" if val is not None else f"{col} IS NULL" for col, val in zip(value_columns, values)])
        query = f"SELECT {key_column} FROM {table_name} WHERE {conditions};"
        cur.execute(query, [val for val in values if val is not None])
        result = cur.fetchone()
        if result:
            return result[0]
        else:
            return None

# Function to insert new author if not already present, and return its primary key
def get_or_create_author(conn, author_name, author_url):
    existing_id = get_id_from_table(conn, 'author', 'author_id', ['author_name', 'author_url'], [author_name, author_url])
    if existing_id:
        return existing_id
    else:
        with conn.cursor() as cur:
            insert_query = f"INSERT INTO author (author_name, author_url) VALUES (%s, %s) RETURNING author_id;"
            cur.execute(insert_query, (author_name, author_url))
            conn.commit()
            return cur.fetchone()[0]
        

# Updated function to insert article data
def insert_article(conn, row):
    # Convert 'NULL' string to None
    for key, value in row.items():
        if value == '':
            row[key] = None

    with conn.cursor() as cur:
        # Retrieve foreign keys from the related tables
        author_id = get_or_create_author(conn, row['author_name'], row.get('author_url'))
        country_id = get_id_from_table(conn, 'country', 'country_id', ['country_name'], [row['country']])
        lang_id = get_id_from_table(conn, 'language', 'lang_id', ['lang_code'], [row['lang']])
        category_id = get_id_from_table(conn, 'category', 'category_id', ['category_name'], [row['category']])
        extractor_id = get_id_from_table(conn, 'extractor', 'extractor_id', ['extractor_name'], ['jeuneafrique'])

        # Insert article data into the article table
        article_query = """
            INSERT INTO article (author_id, country_id, lang_id, category_id, extractor_id, publication_date, title, description, img_url, url, content_preview, content, source)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        cur.execute(article_query, (
            author_id,
            country_id,
            lang_id,
            category_id,
            extractor_id,
            row['publication_date'],
            row['title'],
            row['description'],
            row['image_url'],
            row['url'],
            row['content_preview'],
            row['content'],
            row['source']
        ))
        conn.commit()

# Updated CSV load function to include author_url
def load_csv_to_db(csv_file):

    
    # Connect to your PostgreSQL database
    conn = psycopg2.connect(
        dbname="africa_news_db",
        user="starias",
        password="my_password",
        host="localhost",
        port=5432
    )
    logger.info("Connected to PostgreSQL database")

    try:
        # Read the CSV file
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, quoting=csv.QUOTE_MINIMAL, escapechar='\\')
            logger.info("Read transformed CSV file")
            for row in reader:
                insert_article(conn, row)
    finally:
        conn.close()
    
    logger.info("Completed load process")

 # Get the current datetime
now = datetime.now()

import os
# Get the current datetime
now = datetime.now()
        
# Extract the date in 'YYYY-MM-DD' format and the hour as a two-digit string
formatted_date = now.strftime('%Y-%m-%d')
formatted_hour = now.strftime('%H') 
        
log_file = f"/home/starias/africa_news_api/logs/etl_logs/{formatted_date}/{formatted_hour}/load.txt"
os.makedirs(os.path.dirname(log_file), exist_ok=True)

logger =Logger(log_file=log_file)

logger.info("Started load process")
# Ensure the directory exists; create if not


# Try to get the CSV file with the specified pattern
try:
    csv_files = glob.glob(f'/home/starias/africa_news_api/staging_area/transformed_news/{formatted_date}/{formatted_hour}/*csv')
    # Check if any CSV files were found
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found for the date {formatted_date} and hour {formatted_hour}.")
    
    csv_file = csv_files[0]
    
    #print(f"Loading CSV file: {csv_file}")

    # Run the script
    load_csv_to_db(csv_file)

except FileNotFoundError as e:
    print(e)  # Handle the file not found error gracefully
except Exception as e:
    print(f"An error occurred: {e}")  # Handle any other exceptions