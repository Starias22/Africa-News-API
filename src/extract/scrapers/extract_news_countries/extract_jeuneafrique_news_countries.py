from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

# Set up the WebDriver (Chrome in this case)
driver = webdriver.Chrome()  # Specify other browsers like Firefox if needed
wait = WebDriverWait(driver, 30)  # Explicit wait

# Navigate to the website
driver.get("https://www.jeuneafrique.com/pays/")

countries = None

# Create a CSV file with the current timestamp to avoid overwriting
filename = "/home/starias/africa_news_api/news_countries/jeuneafrique_news_countries.csv"

# Initialize an empty list to store rows
data = []
countries = []



try:
    # Retrieve all the news countries using the WebDriver
    countries_sections= wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.footer-sitemap__list"))
        )
    for section in countries_sections:
        section_countries=section.find_elements(By.CSS_SELECTOR, "a.footer-sitemap__link")
        countries.extend(section_countries)
    print(len(countries))

    print(countries)

    for country in countries:

        country_name = country.get_attribute("textContent").split()
        country_name = " ".join(country_name)

        print(country_name)
        country_url = country.get_attribute("href")
        print(country_name, country_url)

        # Append the country name and URL to the data list
        data.append([country_name, country_url])

except Exception as e:
    print("Error while waiting for news countries:", e)

finally:
    # Open the CSV file for writing
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(["country_name", "country_url"])
        # Write all the rows at once
        writer.writerows(data)

# Close the WebDriver after scraping is done
driver.quit()

print(f"Data saved to {filename}")


