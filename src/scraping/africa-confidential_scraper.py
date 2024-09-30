from selenium.webdriver.common.by import By
from news_scraper import NewsScraper


country_identifier = 3 # Benin
# country_identifier = 34 # Morocco

start_url = f"https://www.africa-confidential.com/browse-by-country/id/{country_identifier}/page/1"
news_item_selector= "#ctl00_cphMain_pnlResults > *"

next_page_identifier=f"a[href='https://www.africa-confidential.com/browse-by-country/id/{country_identifier}/page/#']"

def extract_item_details(news_item,driver=None):
    # Extract the news article URL
    title_url = news_item.find_element(By.CSS_SELECTOR, "h2 a")
    countries = news_item.find_element(By.CSS_SELECTOR, "ul.article-countries li a").text
    print(countries)
    title = title_url.text
    url = title_url.get_attribute("href")
    publication_date = news_item.find_element(By.CSS_SELECTOR, "time.article-date").text
    print(publication_date)
    description = news_item.find_element(By.CSS_SELECTOR, "div.article-subhead").text
    print(description)
    content_preview = news_item.find_element(By.TAG_NAME, "p").text
    print(content_preview)
    news_dict = {
    "title": title,
    "publication_date": publication_date,
    "description": description,
    "url": url,
    "countries": countries,
    "content_preview":content_preview
                }
    print(news_dict)
    return news_dict

scraper = NewsScraper(source="africa-confidential",
                      start_url=start_url,
                      news_item_selector=news_item_selector,
                      extract_item_details=extract_item_details,
                      next_page_identifier=next_page_identifier
                      )
scraper.scrape_news()
