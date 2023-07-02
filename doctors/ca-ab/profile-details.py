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
            with open(file_path, 'r') as json_file:
                try:
                    json_data = json.load(json_file)
                    profile_url = json_data.get('Profile URL')
                    if profile_url:
                        # Open the profile URL
                        browser.get(profile_url)

                        # Add a delay to ensure the entire page loads
                        time.sleep(3)

                        # Wait for the profile page to load
                        wait = WebDriverWait(browser, 10)
                        wait.until(EC.presence_of_element_located((By.ID, 'Tab1Content')))

                        # Scrape the additional data
                        additional_data = {}
                        try:
                            registration_number = browser.find_element(By.XPATH, '//*[@id="Tab1Content"]/div[1]/div[2]/p').text
                            additional_data['Registration Number'] = registration_number
                        except Exception as e:
                            print(f"Error while extracting 'Registration Number' in {file}: {str(e)}")

                        try:
                            gender = browser.find_element(By.XPATH, '//*[@id="Tab1Content"]/div[4]/div[2]/p').text
                            additional_data['Gender'] = gender
                        except Exception as e:
                            print(f"Error while extracting 'Gender' in {file}: {str(e)}")

                        try:
                            specialties = browser.find_element(By.XPATH, '//*[@id="Tab1Content"]/div[6]/div[2]/p').text
                            additional_data['Specialties'] = specialties
                        except Exception as e:
                            print(f"Error while extracting 'Specialties' in {file}: {str(e)}")

                        # Update the JSON file with the new data
                        with open(file_path, 'r+') as updated_json_file:
                            json_data.update(additional_data)
                            updated_json_file.seek(0)
                            json.dump(json_data, updated_json_file, indent=4)
                            updated_json_file.truncate()

                        print(f"Completed processing: {file_path}")

                except (json.JSONDecodeError, AttributeError) as e:
                    # Error occurred while parsing JSON file or accessing attributes
                    print(f"Error while processing {file}: {str(e)}")
