import json
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Specify the path to the chromedriver executable
driver_path = '/path/to/chromedriver'
service = Service(executable_path=driver_path)
browser = webdriver.Chrome(service=service)

# Define the path for the scrapes folder
data_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scrapes')

# Load and process each JSON file
for root, _, files in os.walk(data_folder):
    for file in files:
        if file.endswith(".json"):
            file_path = os.path.join(root, file)
            with open(file_path, 'r+') as json_file:
                try:
                    json_data = json.load(json_file)
                    discipline_url = json_data.get('Discipline URL')
                    if discipline_url:
                        # Open the discipline URL
                        browser.get(discipline_url)

                        # Add a delay to ensure the entire page loads
                        time.sleep(3)

                        # Wait for the page to load
                        wait = WebDriverWait(browser, 10)
                        wait.until(EC.presence_of_element_located((By.ID, 'MainContent_physicianProfileView_pnlDisciplinaryActions')))

                        # Get the elements within the specified XPath
                        elements = browser.find_elements(By.XPATH, '//*[@id="MainContent_physicianProfileView_pnlDisciplinaryActions"]/ul/*')

                        # Extract and append the dates, text, and URLs to the JSON file
                        additional_data = []
                        for element in elements:
                            date_element = element.find_elements(By.TAG_NAME, 'span')
                            link_element = element.find_elements(By.TAG_NAME, 'a')
                            date = date_element[0].text.strip('()') if date_element else None
                            text = element.text.replace(date, "").strip() if date else element.text.strip()
                            link = link_element[0].get_attribute('href') if link_element else None
                            additional_data.append({'Date': date, 'Text': text, 'URL': link})

                        # Append the additional data to the JSON file
                        json_data['DisciplineFiles'] = additional_data
                        if additional_data and additional_data[0]['Date']:
                            json_data['Date'] = additional_data[0]['Date']
                        json_file.seek(0)
                        json.dump(json_data, json_file, indent=4)
                        json_file.truncate()

                        print(f"Appended data to: {file_path}")

                except (json.JSONDecodeError, AttributeError) as e:
                    # Error occurred while parsing JSON file or accessing attributes
                    print(f"Error while processing {file}: {str(e)}")
