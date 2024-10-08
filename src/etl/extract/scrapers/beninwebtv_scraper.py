from selenium.webdriver.common.by import By
from news_scraping import NewsScraper
from urllib.parse import urlparse
import csv

# Initialize an empty list to store the rows from the CSV file
countries_data = []
filename = "/home/starias/africa_news_api/news_countries/beninwebtv_news_countries.csv"


news_item_selector="#tdi_58 > *"

def extract_item_details(news_item, driver=None,country=None):
        news_item_div = news_item.find_element(By.CSS_SELECTOR, "div.tdc-row")
        # Extract the news article URL
        url = news_item_div.find_element(By.TAG_NAME, "a").get_attribute("href")
        image_url = news_item_div.find_element(By.TAG_NAME, "img").get_attribute("src")  # Get image URL

        # Extracting relevant news details
        news_details = news_item_div.find_elements(By.CSS_SELECTOR, "div.wpb_wrapper")
        news_detail = news_details[1]
        country = news_detail.find_element(By.CSS_SELECTOR, "a[data-taxonomy='pays']").text
        title_url = news_detail.find_element(By.TAG_NAME, "h3").find_element(By.TAG_NAME, "a")

        title = title_url.get_attribute("title")
        url = title_url.get_attribute("href")
        description_content = news_detail.find_element(By.CSS_SELECTOR, "div.td_block_wrap.tdb_module_excerpt.tdb_module_excerpt_0").text
        description = description_content.strip()
        category = news_detail.find_element(By.CSS_SELECTOR, "a[data-taxonomy='category']").text
        author_element = news_detail.find_element(By.CSS_SELECTOR, "div.td_block_wrap.tdb_module_author_name.tdb_module_author_name_0 a")
        author_url = author_element.get_attribute("href")
        author_name = author_element.text
        publication_date_elements = news_detail.find_elements(By.TAG_NAME, "time")
        publication_date = publication_date_elements[-1].text if publication_date_elements else None
        news_dict={
            "title": title,
            "author_name": author_name,
            "author_url": author_url,
            "publication_date": publication_date,
            "description": description,
            "category": category,
            "image_url": image_url,
            "url": url,
            "country": country,
            "lang":"fr",
            "content":None,
            "source":None
        }
        return news_dict

scraper = NewsScraper(extractor="beninwebtv",
                      news_item_selector=news_item_selector,
                      extract_item_details=extract_item_details,
                      countries_csv_file = filename,
                      url_second_part="page/#/" 
                      )


scraper.scrape_all_news()