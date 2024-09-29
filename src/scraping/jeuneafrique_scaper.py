from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException




# Initialize the WebDriver
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 30)  # Explicit wait

# Set the country and the maximum number of pages to scrape
country = "benin"  # You can change this to "togo" or "maroc"
max_pages = 10  # Specify the number of pages to scrape
current_page = 1

canceled = False

# Start parsing
try:
    print(f"Starting to parse {country}...")

    driver.get(f"https://www.jeuneafrique.com/pays/{country}/page/{1}")
    driver.implicitly_wait(10)
    

    while True:
        print(current_page)

        try:
            # Retrieve all the news articles using the WebDriver
            news = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[class='teaser-list__item -last:pb-16 -last:border-b first:-mt-16 pt-16']"))
            )
            print("News items found:", len(news))

        except Exception as e:
            print("Error while waiting for news items:", e)
            break

        # Select elements with the exact class name
        #news = driver.find_elements(By.CSS_SELECTOR, "[class='teaser-list__item -last:pb-16 -last:border-b first:-mt-16 pt-16']")
        print(f"Found {len(news)} news items on page {current_page}")

        for news_item in news:
            if not canceled:

                activate_notifications_box = driver.find_element(By.ID, "onesignal-slidedown-container")
                print(activate_notifications_box)
                print("Found****")
                # If the box is found, click the cancel button
                if activate_notifications_box:
                        cancel_button = activate_notifications_box.find_element(By.ID, "onesignal-slidedown-cancel-button")
                        cancel_button.click()
                        canceled = True
                        print("Cancel button clicked")

            #article = news_item.find_element(By.TAG_NAME, "article")

            try:
                article = news_item.find_element(By.TAG_NAME, "article")
            
                image_url = article.find_element(By.CSS_SELECTOR, "a img").get_attribute("src")
            
            except NoSuchElementException:
                print("This is not an article. Continuing to the next news item.")
                continue

            print("Image URL:", image_url)

            article_body = article.find_element(By.CSS_SELECTOR, "div.thumbnail__body")
            title_url = article_body.find_element(By.CSS_SELECTOR, "h4 a")
            title = title_url.find_element(By.CSS_SELECTOR, "span").text
            print("Title:", title)
            url = title_url.get_attribute("href")
            print("URL:",url)



            description = article_body.find_element(By.CSS_SELECTOR, "p").text
            print("Description:", description)

            publication_date = article_body.find_element(By.CSS_SELECTOR, "div.thumbnail__footer span").text
            print("Publication Date:", publication_date)

            print("=" * 40)  # Separator for each news item

        if current_page == max_pages:
            break
        # Increment the current page count
        current_page += 1

        next_page = driver.find_element(By.CSS_SELECTOR, f"a[href='/pays/{country}/page/{current_page}/']")
        print("+++++++++++++",next_page)
        print(f"Accessing page {current_page} for {country}...")
        
        driver.execute_script("arguments[0].click();", next_page)
        
        #next_page.click()
        driver.implicitly_wait(5)
        import time
        time.sleep(0.001)

        

finally:
    print("Cleaning up...")
    driver.quit()  # Close the WebDriver after completion
