from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize the WebDriver
driver = webdriver.Chrome()  # You can specify other browsers like Firefox
wait = WebDriverWait(driver, 30)  # Explicit wait

# Parameters
max_pages = 10
region = "afrique-de-louest"
country_identifier = "benin"
current_page = 1


# Start parsing
try:
    print("Starting Parse")
    driver.get(f"https://beninwebtv.com/pays/afrique/{region}/{country_identifier}/?tdb-loop-page={1}")
    driver.implicitly_wait(10)
    
    # Loop through the pages
    while True:
        print(current_page)
        
        

        try:
            # Retrieve all the news articles using the WebDriver
            news_items = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#tdi_58 > *"))
            )
            print("News items found:", len(news_items))

        except Exception as e:
            print("Error while waiting for news items:", e)
            break

        for news_item in news_items:
            try:
                news_item_div = news_item.find_element(By.CSS_SELECTOR, "div.tdc-row")
                # Extract the news article URL
                url = news_item_div.find_element(By.TAG_NAME, "a").get_attribute("href")
                print("Article URL:", url)

                image_url = news_item_div.find_element(By.TAG_NAME, "img").get_attribute("src")  # Get image URL

                # Extracting relevant news details
                news_details = news_item_div.find_elements(By.CSS_SELECTOR, "div.wpb_wrapper")
                
                if len(news_details) < 2:
                    continue

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

                print({
                    "title": title,
                    "author_name": author_name,
                    "author_url": author_url,
                    "publication_date": publication_date,
                    "description": description,
                    "category": category,
                    "image_url": image_url,
                    "url": url,
                    "country": country
                })

            except Exception as e:
                print("Error processing news item:", e)
        if current_page == max_pages:
            break

        # Increment the current page count
        current_page += 1
        next_page = driver.find_element(By.CSS_SELECTOR, f"a[href='/pays/afrique/{region}/{country_identifier}/?tdb-loop-page={current_page}']")
        print("+++++++++++++",next_page)
        print(f"Accessing page {current_page} for {country}...")
        
        driver.execute_script("arguments[0].click();", next_page)
        driver.implicitly_wait(5)

finally:
    print("Cleaning up...")
    driver.quit()  # Close the WebDriver after completion
