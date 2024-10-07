import csv
import psycopg2
import glob
from datetime import datetime

# Function to retrieve primary key/foreign key from a table
def get_id_from_table(conn, table_name, key_column, value_column, value):
    with conn.cursor() as cur:
        if value:
            query = f"SELECT {key_column} FROM {table_name} WHERE {value_column} = %s;"
            print(query)
            print(value)
            cur.execute(query, (value,))
        else: 
            query = f"SELECT {key_column} FROM {table_name} WHERE {value_column} IS NULL"
            print(query)
            print(value)
            cur.execute(query)
        result = cur.fetchone()
        if result:
            return result[0]
        else:
            return None

# Function to insert new record if not already present, and return its primary key
def get_or_create_id(conn, table_name, key_column, value_column, value):
    existing_id = get_id_from_table(conn, table_name, key_column, value_column, value)
    if existing_id:
        return existing_id
    else:
        with conn.cursor() as cur:
            insert_query = f"INSERT INTO {table_name} ({value_column}) VALUES (%s) RETURNING {key_column};"
            cur.execute(insert_query, (value,))
            conn.commit()
            return cur.fetchone()[0]

# Function to insert article data
def insert_article(conn, row):
    # Convert 'NULL' string to None
    for key, value in row.items():
        if value == '':
            row[key] = None

    with conn.cursor() as cur:
        # Retrieve foreign keys from the related tables
        author_id = get_or_create_id(conn, 'author', 'author_id', 'author_name', row['author_name'])
        country_id = get_id_from_table(conn, 'country', 'country_id', 'country_name', row['countries'])
        lang_id = get_id_from_table(conn, 'language', 'lang_id', 'lang_code', row['lang'])
        category_id = get_id_from_table(conn, 'category', 'category_id', 'category_name', row['category'])
        extractor_id = get_id_from_table(conn, 'extractor', 'extractor_id', 'extractor_name', 'jeuneafrique')
        print("+++++++++++++++++")
        
        print(row)
        print(row['publication_date'])
        print(row['category'])
        print("*****")

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

# Function to load CSV into the database
def load_csv_to_db(csv_file):
    # Connect to your PostgreSQL database
    conn = psycopg2.connect(
        dbname="africa_news_db",
        user="starias",
        password="my_password",
        host="localhost",
        port=5432
    )

    try:
        # Read the CSV file
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, quoting=csv.QUOTE_MINIMAL, escapechar='\\')
            for row in reader:
                insert_article(conn, row)
    finally:
        conn.close()

 # Get the current datetime
now = datetime.now()

# Extract the date in 'YYYY-MM-DD' format and the hour as a two-digit string
formatted_date = now.strftime('%Y-%m-%d')
formatted_hour = now.strftime('%H')  # This will be '02' if the hour is 2


# Try to get the CSV file with the specified pattern
try:
    csv_files = glob.glob(f'/home/starias/africa_news_api/staging_area/transformed_news/{formatted_date}/{formatted_hour}/*csv')
    # Check if any CSV files were found
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found for the date {formatted_date} and hour {formatted_hour}.")
    
    # Get the first CSV file
    csv_file = csv_files[0]
    print(f"Loading CSV file: {csv_file}")

    # Run the script
    load_csv_to_db(csv_file)

except FileNotFoundError as e:
    print(e)  # Handle the file not found error gracefully
except Exception as e:
    print(f"An error occurred: {e}")  # Handle any other exceptions