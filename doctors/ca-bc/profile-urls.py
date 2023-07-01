import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import os
import json

# Specify the folder path for the "scrapes" folder
scrapes_folder = 'scrapes'

# Get the list of subfolders in the "scrapes" folder
subfolders = [folder for folder in os.listdir(scrapes_folder) if os.path.isdir(os.path.join(scrapes_folder, folder))]

# Sort the subfolders by name and get the latest subfolder
latest_subfolder = sorted(subfolders)[-1]

# Create the full path for the latest subfolder
latest_folder = os.path.join(scrapes_folder, latest_subfolder)

# Get the list of JSON files in the latest subfolder
json_files = [file for file in os.listdir(latest_folder) if file.endswith('.json')]

# Configure Selenium to use the appropriate web driver
# Make sure you have the correct web driver executable in your system PATH or provide the path to it
driver = webdriver.Chrome()

# Iterate over each JSON file in the latest subfolder
for json_file in json_files:
    json_path = os.path.join(latest_folder, json_file)

    # Load the JSON data from the file
    with open(json_path) as file:
        data = json.load(file)

    last_name = data['Last Name']
    first_name = data['First Name']

    # Open the search URL
    driver.get("https://www.cpsbc.ca/public/registrant-directory/search-result")

    # Find the Last Name input field and enter the value
    last_name_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH,
                                        '/html/body/div[1]/div/main/div/div/div/div/div[2]/div[3]/div/div/form/div/div[1]/div/div/div[2]/div[1]/input'))
    )
    last_name_field.click()
    last_name_field.clear()
    last_name_field.send_keys(last_name)

    # Find the First Name input field and enter the value
    first_name_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH,
                                        '/html/body/div[1]/div/main/div/div/div/div/div[2]/div[3]/div/div/form/div/div[1]/div/div/div[2]/div[2]/input'))
    )
    first_name_field.click()
    first_name_field.clear()
    first_name_field.send_keys(first_name)

    # Press Enter to submit the search
    first_name_field.send_keys(Keys.ENTER)

    # Wait for a few seconds for the search results to load
    time.sleep(5)  # Increase the delay to 5 seconds

    try:
        url_element = driver.find_element(By.CSS_SELECTOR, 'h5 a')

        url = url_element.get_attribute('href')
        # Store the URL in the JSON data
        data['Profile URL'] = url
        print(f"URL found for {last_name}, {first_name}: {url}")
    except (NoSuchElementException, TimeoutException):
        data['Result URL'] = "No results"
        print(f"No results found for {last_name}, {first_name}")
        continue

    # Save the updated JSON data back to the file
    with open(json_path, 'w') as file:
        json.dump(data, file, indent=4)

# Quit the web driver
driver.quit()

print("Data scraping and JSON update complete.")
