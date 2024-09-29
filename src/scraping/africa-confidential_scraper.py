from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


# Initialize the WebDriver
driver = webdriver.Chrome()  # You can specify other browsers like Firefox
wait = WebDriverWait(driver, 30)  # Explicit wait

# Parameters
max_pages = 100
country_identifier = 3 # Benin
country_identifier = 34 # Morocco
current_page = 1


# Start parsing
try:
    print("Starting Parse")
    driver.get(f"https://www.africa-confidential.com/browse-by-country/id/{country_identifier}/page/1")

    driver.implicitly_wait(10)
    
    # Loop through the pages
    while True:
        print(current_page)
        
        

        try:
            # Retrieve all the news articles using the WebDriver
            news_items = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#ctl00_cphMain_pnlResults > *"))
            )
            print("News items found:", len(news_items))

        except Exception as e:
            print("Error while waiting for news items:", e)
            break

        for news_item in news_items:
            try:
                #news_item_div = news_item.find_element(By.CSS_SELECTOR, "div.tdc-row")
                # Extract the news article URL
                title_url = news_item.find_element(By.CSS_SELECTOR, "h2 a")
                #print("Article URL:", t)

                #image_url = news_item.find_element(By.TAG_NAME, "img").get_attribute("src")  # Get image URL

                # Extracting relevant news details
                #news_details = news_item.find_elements(By.CSS_SELECTOR, "div.wpb_wrapper")
                
                #if len(news_details) < 2:
                    #continue

                news_detail = 0
                countries = news_item.find_element(By.CSS_SELECTOR, "ul.article-countries li a").text
                print("444444444444444444444444444")
                print(countries)
                #title_url = news_detail.find_element(By.TAG_NAME, "h3").find_element(By.TAG_NAME, "a")

                title = title_url.text
                url = title_url.get_attribute("href")
                print("Article URL:", url)
                print("Article title:", title)
                publication_date = news_item.find_element(By.CSS_SELECTOR, "time.article-date").text
                #publication_date = publication_date_element[-1].text if publication_date_elements else None

                print(publication_date)
                print("^^^^^^")

                #description_content = news_detail.find_element(By.CSS_SELECTOR, "div.td_block_wrap.tdb_module_excerpt.tdb_module_excerpt_0").text
                #description = description_content.strip()
                description = news_item.find_element(By.CSS_SELECTOR, "div.article-subhead").text

                print(description)

                content_preview = news_item.find_element(By.TAG_NAME, "p").text

                print(content_preview)

                #category = news_detail.find_element(By.CSS_SELECTOR, "a[data-taxonomy='category']").text

                #author_element = news_detail.find_element(By.CSS_SELECTOR, "div.td_block_wrap.tdb_module_author_name.tdb_module_author_name_0 a")
                #author_url = author_element.get_attribute("href")
                #author_name = author_element.text

                

                print({
                    "title": title,
                    #"author_name": author_name,
                    #"author_url": author_url,
                    "publication_date": publication_date,
                    "description": description,
                    #"category": category,
                    #"image_url": image_url,
                    "url": url,
                    "country": countries,
                    "content_preview":content_preview
                })

            except Exception as e:
                print("Error processing news item:", e)
        if current_page == max_pages:
            break

        # Increment the current page count
        current_page += 1
        try:
            next_page = driver.find_element(By.CSS_SELECTOR, f"a[href='https://www.africa-confidential.com/browse-by-country/id/{country_identifier}/page/{current_page}']")
            print("+++++++++++++",next_page)
            print(f"Accessing page {current_page} for {country_identifier}...")
            
            driver.execute_script("arguments[0].click();", next_page)
            driver.implicitly_wait(5)
        except NoSuchElementException as e:
                print("No more news item")
                break

finally:
    print("Cleaning up...")
    driver.quit()  # Close the WebDriver after completion
