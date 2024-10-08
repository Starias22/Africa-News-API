from selenium.webdriver.common.by import By
from news_scraping import NewsScraper
from urllib.parse import urlparse
import csv

# Initialize an empty list to store the rows from the CSV file
data_from_csv = []
filename = "/home/starias/africa_news_api/news_countries/africa-confidential_news_countries.csv"
# Open the CSV file for reading
with open(filename, mode='r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    # Skip the header row
    next(reader)
    # Read the remaining rows and append them to the list
    for row in reader:
        data_from_csv.append(row)

# Print the data read from the CSV file
print("Data read from CSV file:")
country_identifier = 3 # Benin
# country_identifier = 34 # Morocco

news_item_selector= "#ctl00_cphMain_pnlResults > *"


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
    "country": countries,
    "content_preview":content_preview,
    "lang":"en",
    "content":None,
    "source":None
                }
    print(news_dict)
    return news_dict

scraper = NewsScraper(extractor="africa-confidential",
                      news_item_selector=news_item_selector,
                      extract_item_details=extract_item_details,
                      
                      )

for item in data_from_csv:
    start_url = item[2]
    print(start_url)
    #start_url = f"https://www.africa-confidential.com/browse-by-country/id/{country_identifier}/page/1"
    

    #next_page_identifier = start_url + "?tdb-loop-page=#"
    # Parse the URL
    parsed_url = urlparse(start_url)

    print(parsed_url)

    # Extract the path
    path = parsed_url.path
    print("The path is", path)
    #next_page_identifier=f"a[href='{path}?tdb-loop-page=#']"
    # Replace the last part with "page/"
    new_url = start_url.rsplit('/', 1)[0] + '/page'
    print(new_url)

    next_page_identifier=f"a[href='{new_url}/#']"
    print("**********************************")
    print(next_page_identifier)
    scraper.scrape_news(
         start_url=start_url,
         next_page_identifier=next_page_identifier
    )

"""scraper.scrape_news(start_url=start_url,
                    next_page_identifier=next_page_identifier)"""
