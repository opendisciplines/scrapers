import json
import os
import time
import uuid
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Specify the path to the chromedriver executable
driver_path = '/path/to/chromedriver'
service = Service(executable_path=driver_path)
browser = webdriver.Chrome(service=service)

# Navigate to the webpage
url = 'https://cpsa.ca/albertans/albertan-complaints/discipline-decisions/'
browser.get(url)

# Add a delay to ensure the entire page loads
time.sleep(5)  # adjust the delay time as needed

# Wait for the table to load
wait = WebDriverWait(browser, 10)
table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.table--responsive')))

# Get all the rows in the table
rows = table.find_elements(By.TAG_NAME, 'tr')

# Define the path for the scrapes folder with the latest date
data_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scrapes')
os.makedirs(data_folder, exist_ok=True)

# Load existing JSON files
existing_data = []
for root, _, files in os.walk(data_folder):
    for file in files:
        if file.endswith(".json"):
            with open(os.path.join(root, file)) as json_file:
                existing_data.append(json.load(json_file))

# Create a subfolder with the current date
date_folder = datetime.now().strftime('%Y-%m-%d')
subfolder = os.path.join(data_folder, date_folder)
os.makedirs(subfolder, exist_ok=True)

# Loop through the rows and extract the text and URL values in each cell
for row_index, row in enumerate(rows):
    data = {}
    cells = row.find_elements(By.TAG_NAME, 'td')
    for cell_index, cell in enumerate(cells):
        if cell.find_elements(By.TAG_NAME, 'a'):
            # If cell contains a link, extract the link URL and text
            link = cell.find_element(By.TAG_NAME, 'a').get_attribute('href')
            text = cell.find_element(By.TAG_NAME, 'a').text
            dis_url = link
            profile_url = link.replace('d=true&', '')  # Remove 'd=true&' from the URL
            data['Name'] = text
            data['Discipline URL'] = dis_url
            data['Profile URL'] = profile_url
        else:
            # Otherwise, extract the cell text only
            data[f'cell_{cell_index}'] = cell.text

    # Split the Name into Last Name and First Name
    if 'Name' in data:
        name_parts = data['Name'].split(',')
        last_name = name_parts[0].replace('Dr.', '').strip()
        first_name = name_parts[1].replace('Dr.', '').strip() if len(name_parts) > 1 else ''
        data['Last Name'] = last_name
        data['First Name'] = first_name

    # Check if this row data is already in our existing data
    if data not in existing_data:
        # If not, save it as a new JSON file
        json_file = os.path.join(subfolder, f'{uuid.uuid4()}.json')
        with open(json_file, 'w') as file:
            json.dump(data, file, indent=4)

        print(f"Data exported to {json_file} successfully.")
    else:
        print("Duplicate data. Skipping.")
