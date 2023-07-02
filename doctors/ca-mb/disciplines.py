import os
import json
import uuid
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from datetime import datetime
from dateutil.parser import parse as parse_date

# Set up the driver and navigate to the page with the table
driver = webdriver.Chrome()
driver.get("https://member.cpsm.mb.ca/member/disciplinaryactions")
time.sleep(10)  # wait for 10 seconds

# Find all the table rows
table_rows = driver.find_elements(By.XPATH, "//tr[@class='alternate1 ']")

# Get the latest date for folder organization
latest_date = datetime.now().strftime("%Y-%m-%d")
folder_path = f"scrapes/{latest_date}"

# Create the folder if it doesn't exist
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Loop through the rows and extract the data
for row in table_rows:
    unique_id = str(uuid.uuid4())  # Generate a random unique identifier
    name = row.find_element(By.XPATH, "./td[1]").text
    data_type = row.find_element(By.XPATH, "./td[2]").text.strip()
    publication_url_elements = row.find_elements(By.XPATH, "./td[3]/a")
    publication_urls = [element.get_attribute("href") for element in publication_url_elements if
                        element.get_attribute("href")]
    publication_date_elements = row.find_elements(By.XPATH, "./td[4]")
    publication_dates = [parse_date(element.text).strftime("%Y-%m-%d") for element in publication_date_elements if
                         element.text]

    # Check if any of the data is empty and skip the row if it is
    if not name or not data_type or not publication_urls or not publication_dates:
        continue

    # Split the name into first name and last name
    last_name, first_name = name.split(",", 1)

    # Print the scraping confirmation
    print(f"Data scraped for: {last_name.strip()}, {first_name.strip()}")

    # Create a dictionary with the data
    data_dict = {
        "ID": unique_id,
        "Last Name": last_name.strip(),
        "First Name": first_name.strip(),
        "Type": data_type,
        "Publication Dates": publication_dates,
        "Publication URLs": publication_urls
    }

    # Generate the file path for the JSON file
    file_path = f"{folder_path}/{unique_id}.json"

    # Write the data to a JSON file
    with open(file_path, "w") as json_file:
        json.dump(data_dict, json_file, indent=4)

# Click the "Next Page" arrow to go to the next page of results
while True:
    try:
        next_button = driver.find_element(By.XPATH, "//a[@title='Next Page']")
        next_button.click()
        time.sleep(5)  # wait for 5 seconds
        table_rows = driver.find_elements(By.XPATH, "//tr[@class='alternate1 ']")

        # Loop through the rows and extract the data
        for row in table_rows:
            unique_id = str(uuid.uuid4())  # Generate a random unique identifier
            name = row.find_element(By.XPATH, "./td[1]").text
            data_type = row.find_element(By.XPATH, "./td[2]").text.strip()
            publication_url_elements = row.find_elements(By.XPATH, "./td[3]/a")
            publication_urls = [element.get_attribute("href") for element in publication_url_elements if
                                element.get_attribute("href")]
            publication_date_elements = row.find_elements(By.XPATH, "./td[4]")
            publication_dates = [parse_date(element.text).strftime("%Y-%m-%d") for element in publication_date_elements if
                                 element.text]

            # Check if any of the data is empty and skip the row if it is
            if not name or not data_type or not publication_urls or not publication_dates:
                continue

            # Split the name into first name and last name
            last_name, first_name = name.split(",", 1)

            # Print the scraping confirmation
            print(f"Data scraped for: {last_name.strip()}, {first_name.strip()}")

            # Create a dictionary with the data
            data_dict = {
                "ID": unique_id,
                "Last Name": last_name.strip(),
                "First Name": first_name.strip(),
                "Type": data_type,
                "Publication Dates": publication_dates,
                "Publication URLs": publication_urls
            }

            # Generate the file path for the JSON file
            file_path = f"{folder_path}/{unique_id}.json"

            # Write the data to a JSON file
            with open(file_path, "w") as json_file:
                json.dump(data_dict, json_file, indent=4)

    except:
        break

# Clean up
driver.quit()
