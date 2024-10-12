import json
import pandas as pd
from datetime import datetime, timedelta
import pytz
from newsapi import NewsApiClient
from GoogleNews import GoogleNews
import os
from pathlib import Path
import sys
import csv
from datetime import datetime

# Add the `src` directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))
from src.logs.log import Logger
from src.config.config import ETL_LOGS_PATH, STAGING_AREA_PATH

# Add 'src' directory to the Python path
src_path = Path(__file__).resolve().parents[2]
sys.path.append(str(src_path))
import os

NEWSAPI_KEYS=[ "f6cca8a85c1e4114b05f78c1e2c4edae",
              "8308c1e8b30640468c1be43719b78124",
              "1b13a2bb468b4f5e959edf839a9cb469",
              " b95752dfc6374f0c9512b9f033ac4b42",
              "8292c7e310214de09a349331fc9fa210",
]

NULL_REPLACEMENTS = {
        "":None,
        "[Removed]": None,  
        "https://removed.com": None
}
LANGUAGES = ["en","fr"]

"""QUERY = [
    "Algeria", "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi",
    "Cabo Verde", "Cameroon", "Central African Republic", "Chad", "Comoros",
    "Congo (Congo-Brazzaville)", "Democratic Republic of the Congo",
    "Djibouti", "Egypt", "Equatorial Guinea", "Eritrea", "Eswatini (Swaziland)",
    "Ethiopia", "Gabon", "Gambia", "Ghana", "Guinea", "Guinea-Bissau", "Ivory Coast (Côte d'Ivoire)",
    "Kenya", "Lesotho", "Liberia", "Libya", "Madagascar", "Malawi", "Mali", "Mauritania", "Mauritius",
    "Morocco", "Mozambique", "Namibia", "Niger", "Nigeria", "Rwanda", "São Tomé and Príncipe", 
    "Senegal", "Seychelles", "Sierra Leone", "Somalia", "South Africa", "South Sudan", 
    "Sudan", "Tanzania", "Togo", "Tunisia", "Uganda", "Zambia", "Zimbabwe"
]"""


QUERY = [
    "Benin", "Morocco", "Botswana", "Burkina Faso", "Burundi",
    "Cabo Verde", "Cameroon", "Central African Republic", "Chad", "Comoros",
    "Congo (Congo-Brazzaville)", "Democratic Republic of the Congo",
    "Djibouti", "Egypt", "Equatorial Guinea", "Eritrea", "Eswatini (Swaziland)",
    "Ethiopia", "Gabon", "Gambia", "Ghana", "Guinea", "Guinea-Bissau", "Ivory Coast (Côte d'Ivoire)",
    "Kenya", "Lesotho", "Liberia", "Libya", "Madagascar", "Malawi", "Mali", "Mauritania", "Mauritius",
    "Mozambique", "Namibia", "Niger", "Nigeria", "Rwanda", "São Tomé and Príncipe", 
    "Senegal", "Seychelles", "Sierra Leone", "Somalia", "South Africa", "South Sudan", 
    "Sudan", "Tanzania", "Togo", "Tunisia", "Uganda", "Zambia", "Zimbabwe"
]


PAGE_SIZE = 100
HOURS_PERIOD = 25

PAGE = 1


class NewsAPIFetcher:
    def __init__(self,extractor):


        self.page=PAGE
        self.page_size=PAGE_SIZE
        self.null_replacements=NULL_REPLACEMENTS
        self.languages=LANGUAGES
        self.query=QUERY
        self.page=self.page       
        
        # Initialize NewsAPI client
        self.newsapi = NewsApiClient(api_key=NEWSAPI_KEYS[2])
        
        # Get current time in UTC
        self.now = datetime.now(pytz.utc)

        # Calculate the time one day ago
        self.period_ago = self.now - timedelta(hours=25)
        
        # Format the dates in the required format
        self.from_param = self.period_ago.strftime('%Y-%m-%dT%H:%M:%S')
        self.to = self.now.strftime('%Y-%m-%dT%H:%M:%S')
        self.extractor = extractor

        # Get the current datetime
        now = datetime.now()
        # Extract the date in 'YYYY-MM-DD' format and the hour as a two-digit string
        formatted_date = now.strftime('%Y-%m-%d')
        formatted_hour = now.strftime('%H')  # This will be '02' if the hour is 2

        #log_file = f"/home/starias/africa_news_api/logs/etl_logs/{formatted_date}/{formatted_hour}/extract/{extractor}.txt"
        #log_file = f"/home/starias/africa_news_api/logs/etl_logs/{formatted_date}/{formatted_hour}/extract/{extractor}.txt"
        log_file = f"{ETL_LOGS_PATH}/{formatted_date}/{formatted_hour}/extract/{extractor}.txt"

        # Ensure the directory exists; create if not
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

        self.logger = Logger(log_file=log_file)
        self.logger.info(f"Started {extractor} extractor")
        

    def save(self, articles):
        
        pass
        
        news = []

        for _, article in articles.iterrows():
            #print(article)
            
            standardized_news = {
                "title": article['title'],
                "description": article['description'],
                "content": article["content"],
                "source": article.get('source_name', None),
                "url": article['url'],
                "image_url": article['img_url'],
                "publication_date": article['publication_date'],
                "lang": article['lang'],
                "author_name":article['author'],
                "extractor":self.extractor,
                "country": article["country"]
            }
            news.append(standardized_news)
        # Define the CSV header
        csv_header = ["title", "author_name", "author_url", "publication_date", 
                      "description", "category", "image_url", "url", "country",
                        "content_preview", "extractor", "lang","content","source"]
        
        # Get the current datetime
        now = datetime.now()
        
        # Extract the date in 'YYYY-MM-DD' format and the hour as a two-digit string
        formatted_date = now.strftime('%Y-%m-%d')
        formatted_hour = now.strftime('%H')  # This will be '02' if the hour is 2
        
        #filepath = f'/home/starias/africa_news_api/staging_area/raw_news/{formatted_date}/{formatted_hour}/{self.extractor}.csv'
        filepath = f'{STAGING_AREA_PATH}/raw_news/{formatted_date}/{formatted_hour}/{self.extractor}.csv'
        # Ensure the directory exists; create if not
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=csv_header, quotechar='"', escapechar='\\')
            writer.writeheader()
            
            # Write the news data
            writer.writerows(news)
            file.close()
        self.logger.info(f"Written header to CSV file: {filepath}")
            


    def fetch_articles(self, extracor, lang, query):
        if extracor == 'google_news':
            googlenews = GoogleNews(period='25h', lang=lang)
            #print(googlenews)
            googlenews.search(query)
            results = googlenews.result()
            #print(results)
            googlenews.clear()
            return results
        elif extracor == 'newsapi':
            response = self.newsapi.get_everything(
                q=query,
                from_param=self.from_param,
                to=self.to,
                language=lang,
                sort_by='relevancy',
                page=self.page,
                page_size=self.page_size
            )
            return response['articles'] if response['status'] == 'ok' else []
        else:
            raise ValueError("Unknown news source")

    def process_articles(self, articles, source):
        articles_df = pd.DataFrame(articles)
        if source == 'google_news':
            articles_df.rename(columns={
            'urlToImage': 'img_url',
            'datetime': 'publication_date',
            'link': 'url',
            'img': 'img_url',
            'desc': 'description',
            'media': 'source_name'
            }, inplace=True)
            articles_df['author'] = None


            articles_df['publication_date'] = articles_df['publication_date'].apply(lambda x: int(x.timestamp()) if pd.notna(x) else None)
            articles_df['content']= None
        elif source == 'newsapi':
            articles_df.rename(columns={
            'urlToImage': 'img_url',
            'publishedAt': 'publication_date'
            }, inplace=True)
            fmt = "%Y-%m-%dT%H:%M:%SZ"
            articles_df['publication_date'] = articles_df['publication_date'].apply(lambda x: int(datetime.strptime(x, fmt).timestamp()))
            articles_df['source'] = articles_df['source'].apply(lambda x: x['name'] if x else None)
            articles_df.drop(columns=['source'], inplace=True)
        
        articles_df.replace(self.null_replacements, inplace=True)
        return articles_df

    def run(self):
        articles_list = []
        num_results_dict = {}
        total_results = 0
        languages=self.languages
        queries=self.query
        i = 1
        for lang in languages[:1]:
            self.logger.info(f"\t\tFetching news for {lang} language")
            results = []
            for query in queries[:3]:
                self.logger.info(f"\t\t\t\t{query} [{i}/{len(queries[:10])}]")
                articles = self.fetch_articles(self.extractor, lang, query)
                if articles:
                    for article in articles:
                        article["country"] = query
                    results.extend(articles)
                    #print("********")
                    #print(results)
                i += 1
            
            if results:
                processed_articles = self.process_articles(results, self.extractor)
                processed_articles['lang'] = lang
                articles_list.append(processed_articles)
                num_results_dict[lang] = len(processed_articles)
                total_results += len(processed_articles)
        
        if articles_list:
            all_articles = pd.concat(articles_list, axis=0, ignore_index=True)
        else:
            all_articles = pd.DataFrame()
        #print(all_articles)
        self.save(all_articles)
        self.logger.info("Written news into CSV file")
        self.logger.info(f"Completed {self.extractor} extractor")
