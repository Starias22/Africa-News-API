from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import os
import sys
from datetime import datetime
from selenium.webdriver.chrome.options import Options as ChromeOptions
# Add the `src` directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))
from src.logs.log import Logger

class NewsScraper:

    def __init__(self, 
                extractor, 
                news_item_selector,
                extract_item_details,
                url_second_part,
                max_pages=1,
                
                countries_csv_file=None,
                
                ):
        
        # Get the current datetime
        now = datetime.now()
        # Extract the date in 'YYYY-MM-DD' format and the hour as a two-digit string
        formatted_date = now.strftime('%Y-%m-%d')
        formatted_hour = now.strftime('%H')  # This will be '02' if the hour is 2

        log_file = f"/home/starias/africa_news_api/logs/etl_logs/{formatted_date}/{formatted_hour}/extract/{extractor}.txt"
        # Ensure the directory exists; create if not
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

        self.logger = Logger(log_file=log_file)
        self.logger.info(f"Started {extractor} extractor")
        

        
        filepath = f'/home/starias/africa_news_api/staging_area/raw_news/{formatted_date}/{formatted_hour}/{extractor}.csv'
        # Ensure the directory exists; create if not
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        self.file= open(filepath, mode='w', newline='', encoding='utf-8')
        
        csv_header = ["title", "author_name", "author_url", "publication_date", "description", "category", "image_url", "url", "country", "content_preview", 
                      "extractor", "lang", "content", "source"
                      ]
        self.writer = csv.DictWriter(self.file, fieldnames=csv_header)
        
        # Write the header to the file
        self.writer.writeheader()
        self.logger.info(f"Written header to CSV file: {filepath}")
        self.countries_data= self.get_countries_data(countries_csv_file)

        self.logger.info(f"Got countries data (names and URLs) from countries CSV file:{countries_csv_file}")

        # Set up Chrome options for headless mode
        #chrome_options = ChromeOptions()
        #chrome_options.add_argument("--headless")  # Run in headless mode
        #chrome_options.add_argument("--no-sandbox")
        #chrome_options.add_argument("--disable-dev-shm-usage")
        #chrome_options.add_argument("--no-startup-window")


        # Initialize the WebDriver with the options
        #self.driver = webdriver.Chrome(options=chrome_options)

        # Initialize the WebDriver
        self.driver = webdriver.Chrome()  # You can specify other browsers like Firefox
        self.wait = WebDriverWait(self.driver, 30)  # Explicit wait
        self.logger.info(f"Innitialized web driver")
        self.current_page = 1
        self.max_pages = max_pages
        self.extract_item_details=extract_item_details
        self.news_item_selector=news_item_selector
        #self.next_page_identifier = next_page_identifier
        self.extractor = extractor
        self.current_country_num = 1
        self.url_second_part = url_second_part
        
        
    def get_countries_data(self, filename):
        countries_data = []
        #filename = "/home/starias/africa_news_api/news_countries/beninwebtv_news_countries.csv"
        # Open the CSV file for reading
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            # Skip the header row
            next(reader)
            # Read the remaining rows and append them to the list
            for row in reader:
                countries_data.append(row)
        return countries_data

    def get_news_items(self):
        news_items = None
        #print("selector",self.news_item_selector)
        try:
            # Retrieve all the news articles using the WebDriver
            news_items = self.wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, self.news_item_selector))
            )
            #print("News items found:", len(news_items))
            #self.logger.info(f"Found {len(news_items)} news items")

        except Exception as e:
            print("Error while waiting for news items:", e)
            self.logger.error(f"Error while waiting for news items: {e}")
            
        return news_items

    
    def record_row(self, row):
        # Define the CSV header
        row["extractor"] = self.extractor
        # Write the news data
        self.writer.writerow(row)
    
    def access_next_page(self, next_page):
        self.driver.execute_script("arguments[0].click();", next_page)
        self.driver.implicitly_wait(5)
    
    def scrape_current_page(self):
        news_items = self.get_news_items()
        #print(news_items)
        #print("******************")
        for news_item in news_items:
            try:
                #print(self.current_country_num-2)
                news_row = self.extract_item_details(news_item, self.driver, self.countries_data[self.current_country_num-2][0])
                self.record_row(news_row)
            except Exception as e:
                print("Error processing news item:", e)
    
    def next_country(self):
        country_name = self.countries_data[self.current_country_num-1][0]
        self.logger.info(f"\t\t\t{country_name}  [{self.current_country_num}/{len(self.countries_data)}]")
        self.current_country_num +=1
        
    def scrape_news(self,start_url=None, next_page_identifier=None):

        if start_url and next_page_identifier:
            self.start_url = start_url
            self.next_page_identifier = next_page_identifier
        
        #print("Starting Parse")
        self.driver.get(self.start_url)
        self.driver.implicitly_wait(10)

        while True:
            self.scrape_current_page()
            if self.current_page == self.max_pages:
                break
            # Increment the current page count
            self.current_page += 1
            next_page = self.driver.find_element(By.CSS_SELECTOR, self.next_page_identifier.replace("#", str(self.current_page)))
            print(f"Accessing page {self.current_page}/{self.max_pages}")        
            self.access_next_page(next_page)
        
    
    def scrape_all_news(self):

        
        num_countries = len(self.countries_data)
        self.logger.info(f"Scraping news for {num_countries} countries")


        for country_row in self.countries_data:
            country_start_url = country_row[1]
            #country_name= country_row[0]
            self.next_country()
            #next_page_identifier = country_start_url + r
            # Parse the URL and extract the path
            path = urlparse(country_start_url).path
            print("*********************",path)
            #print("The path is", path)
            next_page_identifier=f"a[href='{path}{self.url_second_part}']"  #f"a[href='{path}page/#/']"
            print(self.extractor)
            if self.extractor == "africa-confidential":
                print("+++++++++++++")
                new_url = country_start_url.rsplit('/', 1)[0] + '/page'
                #print("The new URL is",new_url)

                next_page_identifier=f"a[href='{new_url}/#']"

            self.scrape_news(
                start_url=country_start_url,
                next_page_identifier=next_page_identifier
            )
            
        self.logger.info(f"Completed {self.extractor} extractor")

    def __del__(self):
        
        self.driver.quit()  # Close the WebDriver after completion
        self.file.close()   
        #self.logger.info(f"Completed {self.extractor} extractor")
