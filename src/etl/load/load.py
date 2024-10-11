from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import csv
import os
import glob
import sys
# Add the `src` directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from src.logs.log import Logger
from src.db.database import *


# Utility functions
def get_or_create_author(session, author_name, author_url):
    author = session.query(Author).filter_by(author_name=author_name, author_url=author_url).first()
    if author:
        return author
    else:
        new_author = Author(author_name=author_name, author_url=author_url)
        session.add(new_author)
        session.commit()
        return new_author
    
def get_or_create_source(session, source_name):
    source = session.query(Source).filter_by(source_name=source_name).first()
    #print(source)
    if source:
        #print("YEEEEEH")
        return source
    else:
        new_source = Source(source_name=source_name)
        session.add(new_source)
        session.commit()
        #print(new_source)
        return new_source

def get_or_create_category(session, category_name, logger):
    category = session.query(Category).filter_by(category_name=category_name).first()
    if category:
        return category
    else:
        new_category = Category(category_name=category_name)
        session.add(new_category)
        session.commit()
        logger.info(f"Added a new category [{category_name}] to the news category table")
        return new_category

def get_extractor(session, extractor_name):
    extractor = session.query(Extractor).filter_by(extractor_name=extractor_name).first()
    return extractor

def get_country(session, country):
    country = session.query(Country).filter_by(country_name=country).first()
    return country

def get_language(session, lang_code):
    language = session.query(Language).filter_by(lang_code=lang_code).first()
    return language




def insert_article(session, row, logger):
    for key, value in row.items():
        if value == '':
            row[key] = None
            
    author = get_or_create_author(session, row['author_name'], row.get('author_url'))
    category = get_or_create_category(session, row['category'], logger=logger)
    extractor = get_extractor(session, row['extractor']) 
    source = get_or_create_source(session, row['source'])
    

    # Fetch country_id and lang_id
    country = get_country(session, row['country'])
    lang = get_language(session, row['lang'])

    country_id = country.country_id if country else None
    lang_id = lang.lang_id if lang else None
    #source_id = source.source_id if source else None

    # Check if the article already exists
    existing_article = session.query(Article).filter_by(
        author_id=author.author_id,
        category_id=category.category_id,
        extractor_id=extractor.extractor_id,
        country_id=country_id,
        lang_id=lang_id,
        source_id=source.source_id,
        title=row['title'],
        url=row['url'],
        img_url=row["image_url"],
        description=row["description"],
        publication_date=row['publication_date'],
        content_preview=row['content_preview'],
        content=row['content']
    ).first()

    if not existing_article:
        
        new_article = Article(
            author_id=author.author_id,
            country_id=country_id,  # Use country_id
            lang_id=lang_id,        # Use lang_id
            category_id=category.category_id,
            extractor_id=extractor.extractor_id,
            source_id=source.source_id,
            publication_date=row['publication_date'],
            title=row['title'],
            description=row['description'],
            img_url=row['image_url'],
            url=row['url'],
            content_preview=row['content_preview'],
            content=row['content'],
        )
        session.add(new_article)
        session.commit()

def load_csv_to_db(csv_file, logger):
    engine = create_engine('postgresql+psycopg2://starias:my_password@localhost:5432/africa_news_db')
    Session = sessionmaker(bind=engine)
    session = Session()

    logger.info("Connected to PostgreSQL ")
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, quoting=csv.QUOTE_MINIMAL, escapechar='\\')
            logger.info("Read transformed CSV file")
            logger.info("**********Loading data into postgreSQL**********")
            for row in reader:
                #print(row)  # Debug line
                insert_article(session, row, logger=logger)
            logger.info("**********Completed**********")
    finally:
        session.close()
        logger.info("Closed PostreSQL session")
    


# Function to initiate the load process
def load(formatted_date=None, formatted_hour=None):
    
    if formatted_date is None and formatted_hour is None:
        now = datetime.now()
        formatted_date = now.strftime('%Y-%m-%d')
        formatted_hour = now.strftime('%H')
    
    log_file = f"/home/starias/africa_news_api/logs/etl_logs/{formatted_date}/{formatted_hour}/load.txt"
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    logger = Logger(log_file=log_file)
    logger.info("Started load process")

    try:
        csv_files = glob.glob(f'/home/starias/africa_news_api/staging_area/transformed_news/{formatted_date}/{formatted_hour}/*csv')
        if not csv_files:
            logger.error(f"No CSV files found for the date {formatted_date} and hour {formatted_hour}.")
        
        csv_file = csv_files[0]
        load_csv_to_db(csv_file, logger=logger)
    except FileNotFoundError as e:
        logger.error(e)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    logger.info("Completed load process")

# Example usage
load(formatted_date="2024-10-09", formatted_hour="06")
