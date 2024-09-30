from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv



#title,author_name,author_url,publication_date,description,category,image_url,url,countries
class NewsScraper:

    def __init__(self, start_url, 
                 news_item_selector, 
                 extract_item_details,
                 next_page_identifier,
                filepath = '/home/starias/africa_news_api/src/staging_area/extracted_news.csv',):
        self.file= open(filepath, mode='a', newline='', encoding='utf-8')
        # Initialize the WebDriver
        self.driver = webdriver.Chrome()  # You can specify other browsers like Firefox
        self.wait = WebDriverWait(self.driver, 30)  # Explicit wait
        self.current_page = 1
        self.max_pages = 2
        self.extract_item_details=extract_item_details
        self.news_item_selector=news_item_selector
        self.start_url=start_url
        self.next_page_identifier = next_page_identifier


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
        csv_header = ["title", "author_name", "author_url", "publication_date", "description", "category", "image_url", "url", "countries"]
        writer = csv.DictWriter(self.file, fieldnames=csv_header)
        # Write the news data
        writer.writerow(row)
    
    def access_next_page(self, next_page):
        self.driver.execute_script("arguments[0].click();", next_page)
        self.driver.implicitly_wait(5)
    
    def scrape_current_page(self):
        news_items = self.get_news_items()
        for news_item in news_items:
            try:
                news_row = self.extract_item_details(news_item)
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
            next_page = self.driver.find_element(By.CSS_SELECTOR, next_page_identifier.replace("#", str(self.current_page)))
            print(f"Accessing page {self.current_page}/{self.max_pages}")        
        self.access_next_page(next_page) 

    def __del__(self):
        print("Cleaning up...")
        self.driver.quit()  # Close the WebDriver after completion
        self.file.close()   


region = "afrique-de-louest"
country_identifier = "benin"

start_url = f"https://beninwebtv.com/pays/afrique/{region}/{country_identifier}/?tdb-loop-page=1"
news_item_selector="#tdi_58 > *"


def extract_item_details(news_item):
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
            "countries": country
        }
        return news_dict

next_page_identifier=f"a[href='/pays/afrique/{region}/{country_identifier}/?tdb-loop-page=#']"

scraper = NewsScraper(start_url=start_url,
                      news_item_selector=news_item_selector,
                      extract_item_details=extract_item_details,
                      next_page_identifier=next_page_identifier
                      )
scraper.scrape_news()

