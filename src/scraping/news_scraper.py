from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv


#title,author_name,author_url,publication_date,description,category,image_url,url,countries,content_preview,source

class NewsScraper:

    def __init__(self, 
                source,
                start_url, 
                news_item_selector,
                next_page_identifier,
                extract_item_details,
                ):
        filepath = f'/home/starias/africa_news_api/src/staging_area/raw_news/{source}.csv'
        self.file= open(filepath, mode='w', newline='', encoding='utf-8')
        # Initialize the WebDriver
        self.driver = webdriver.Chrome()  # You can specify other browsers like Firefox
        self.wait = WebDriverWait(self.driver, 30)  # Explicit wait
        self.current_page = 1
        self.max_pages = 2
        self.extract_item_details=extract_item_details
        self.news_item_selector=news_item_selector
        self.start_url=start_url
        self.next_page_identifier = next_page_identifier
        self.source = source
        csv_header = ["title", "author_name", "author_url", "publication_date", "description", "category", "image_url", "url", "countries", "content_preview", 
                      #"source"
                      ]
        self.writer = csv.DictWriter(self.file, fieldnames=csv_header)
        
        #row["source"] = self.source
        # Write the header to the file
        self.writer.writeheader()
        


    def get_news_items(self):
        news_items = None
        try:
            # Retrieve all the news articles using the WebDriver
            news_items = self.wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, self.news_item_selector))
            )
            print("News items found:", len(news_items))

        except Exception as e:
            print("Error while waiting for news items:", e)
            
        return news_items

    
    def record_row(self, row):
        # Define the CSV header
        
        # Write the news data
        self.writer.writerow(row)
    
    def access_next_page(self, next_page):
        self.driver.execute_script("arguments[0].click();", next_page)
        self.driver.implicitly_wait(5)
    
    def scrape_current_page(self):
        news_items = self.get_news_items()
        for news_item in news_items:
            try:
                news_row = self.extract_item_details(news_item, self.driver)
                self.record_row(news_row)
            except Exception as e:
                print("Error processing news item:", e)
        
    def scrape_news(self):
        print("Starting Parse")
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

    def __del__(self):
        print("Cleaning up...")
        self.driver.quit()  # Close the WebDriver after completion
        self.file.close()   
