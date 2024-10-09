from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
from urllib.parse import urlsplit

# Set up the WebDriver (Chrome in this case)
driver = webdriver.Chrome()  # Specify other browsers like Firefox if needed
wait = WebDriverWait(driver, 30)  # Explicit wait

# Navigate to the website
driver.get("https://www.africa-confidential.com/")

countries = None

# Create a CSV file with the current timestamp to avoid overwriting
filename = "/home/starias/africa_news_api/news_countries/africa-confidential_news_countries.csv"

# Initialize an empty list to store rows
data = []




try:
    # Retrieve all the news countries using the WebDriver
    countries_nav = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "nav.column.medium-66"))
    )[0]

    print(countries_nav)

    countries = countries_nav.find_elements(By.CSS_SELECTOR, "a.row")

    for country in countries:
        # Extract country name and URL
        country_name = country.text
        country_url = country.get_attribute("href")

        url_parts = urlsplit(country_url)

        # Reconstruct the base URL excluding the last part
        print(country_url)

        country_identifier = country_url.split('/')[-1]  # Get the second to last part
        print(country_identifier)
        print(country_name, country_url)
        

        # Append the country name and URL to the data list
        data.append([country_identifier, country_url, country_name])

        print(country_identifier, country_name, country_url)
        
except Exception as e:
    print("Error while waiting for news countries:", e)

finally:
    # Open the CSV file for writing
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(["country_identifier", "country_url", "country_name"])  # Write all the rows at once
        writer.writerows(data)

# Close the WebDriver after scraping is done
driver.quit()

print(f"Data saved to {filename}")
