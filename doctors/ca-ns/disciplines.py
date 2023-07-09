import os
import json
import uuid
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up the Selenium driver (assuming you have ChromeDriver installed)
driver = webdriver.Chrome()

# Open the website
driver.get('https://cpsns.ns.ca/complaints-investigations/directory-of-disciplinary-decisions/')

# Find and click through each page
page = 1
while True:
    # Wait for the <tbody> element to be present
    tbody = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'tbody')))

    # Find all rows within the <tbody> element
    rows = tbody.find_elements(By.TAG_NAME, 'tr')

    # Process each row
    for row in rows:
        # Extract data points from each cell
        cells = row.find_elements(By.TAG_NAME, 'td')
        date = cells[0].text

        # Check if the <span> element exists in the cell
        name_element = cells[1].find_elements(By.TAG_NAME, 'span')
        name = name_element[0].text if name_element else ""

        complaint_element = cells[2].find_elements(By.TAG_NAME, 'span')
        complaint = complaint_element[0].text if complaint_element else ""

        outcome = cells[3].text

        # Check if the <a> tag exists in the cell
        announcement_url_element = cells[4].find_elements(By.TAG_NAME, 'a')
        announcement_url = announcement_url_element[0].get_attribute('href') if announcement_url_element else ""

        discipline_url_element = cells[5].find_elements(By.TAG_NAME, 'a')
        discipline_url = discipline_url_element[0].get_attribute('href') if discipline_url_element else ""

        # Create a unique filename for the JSON file
        filename = str(uuid.uuid4())

        # Create a dictionary to store the data
        data = {
            'date': date,
            'name': name,
            'complaint': complaint,
            'outcome': outcome,
            'announcement_url': announcement_url,
            'discipline_url': discipline_url
        }

        # Convert the data to JSON
        json_data = json.dumps(data)

        # Specify the absolute file path to store the JSON files
        file_path = os.path.abspath(os.path.join(os.getcwd(), "scrapes", f"{filename}.json"))
        with open(file_path, 'w') as file:
            file.write(json_data)

        # Print the row of data
        print(f"Row Data: {data}")
        print()

    # Break if we've reached the desired number of pages (11 in this case)
    if page == 11:
        break

    # Find the Next button and click it
    next_button_xpath = '/html/body/div[3]/main/section/div[2]/div/div[2]/div[2]/a[2]'
    next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, next_button_xpath)))
    driver.execute_script("arguments[0].click();", next_button)

    # Add a wait timer to allow the page to load fully
    time.sleep(2)  # Adjust the duration as needed (e.g., 1 second, 3 seconds)

    # Increment the page counter
    page += 1

# Close the browser
driver.quit()
