from selenium.webdriver.common.by import By
from news_scraping import NewsScraper
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from news_scraping import NewsScraper
from urllib.parse import urlparse
import csv


"""# Initialize an empty list to store the rows from the CSV file
data_from_csv = []

# Open the CSV file for reading
with open(filename, mode='r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    # Skip the header row
    next(reader)
    # Read the remaining rows and append them to the list
    for row in reader:
        data_from_csv.append(row)"""

# Print the data read from the CSV file
#print("Data read from CSV file:")


filename = "/home/starias/africa_news_api/news_countries/jeuneafrique_news_countries.csv"

news_item_selector= "[class='teaser-list__item -last:pb-16 -last:border-b first:-mt-16 pt-16']"

canceled = False
def extract_item_details(news_item, driver, country):
    global canceled
    if not canceled:
        activate_notifications_box = driver.find_element(By.ID, "onesignal-slidedown-container")
        # If the box is found, click the cancel button
        if activate_notifications_box:
            cancel_button = activate_notifications_box.find_element(By.ID, "onesignal-slidedown-cancel-button")
            cancel_button.click()
            canceled = True
            #print("Cancel button clicked")

    try:
        article = news_item.find_element(By.TAG_NAME, "article")
            
        image_url = article.find_element(By.CSS_SELECTOR, "a img").get_attribute("src")
            
    except NoSuchElementException:
        print("This is not an article. Continuing to the next news item.")
        #continue

    article_body = article.find_element(By.CSS_SELECTOR, "div.thumbnail__body")
    title_url = article_body.find_element(By.CSS_SELECTOR, "h4 a")
    title = title_url.find_element(By.CSS_SELECTOR, "span").text
    url = title_url.get_attribute("href")
    description = article_body.find_element(By.CSS_SELECTOR, "p").text
    publication_date = article_body.find_element(By.CSS_SELECTOR, "div.thumbnail__footer span").text
    #print("=" * 40)  # Separator for each news item
    news_dict = {
        "title": title,
        "publication_date": publication_date,
        "description": description,
        "image_url": image_url,
        "url": url,
        "country": country,
        "lang":"fr",
        "content":None,
        "source":None
        }
    #print(news_dict)
    return news_dict



scraper = NewsScraper(extractor="jeuneafrique",
                      news_item_selector=news_item_selector,
                      extract_item_details=extract_item_details,
                      countries_csv_file = filename,
                      url_second_part="?tdb-loop-page=#"
                      )

scraper.scrape_all_news()

"""for item in data_from_csv:
    start_url = item[1]
    country = item[0]
    # Parse the URL
    parsed_url = urlparse(start_url)

    # Extract the path
    path = parsed_url.path
    next_page_identifier=f"a[href='{path}page/#/']"
    scraper.scrape_news(
         start_url=start_url,
         next_page_identifier=next_page_identifier
    )"""