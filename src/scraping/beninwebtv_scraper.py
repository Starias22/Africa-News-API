from selenium.webdriver.common.by import By
from news_scraper import NewsScraper

region = "afrique-de-louest"
country_identifier = "benin"

start_url = f"https://beninwebtv.com/pays/afrique/{region}/{country_identifier}/?tdb-loop-page=1"
news_item_selector="#tdi_58 > *"

def extract_item_details(news_item, driver=None):
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

scraper = NewsScraper(source="beninwebtv",
                      start_url=start_url,
                      news_item_selector=news_item_selector,
                      extract_item_details=extract_item_details,
                      next_page_identifier=next_page_identifier
                      )
scraper.scrape_news()

