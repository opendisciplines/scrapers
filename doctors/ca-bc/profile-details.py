import requests
from bs4 import BeautifulSoup
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

# Iterate over each JSON file in the latest folder
for json_file in json_files:
    json_path = os.path.join(latest_folder, json_file)

    # Load the JSON data from the file
    with open(json_path) as file:
        data = json.load(file)

    # Skip if the JSON file doesn't have a Profile URL
    if 'Profile URL' not in data:
        print(f"Skipping JSON file without Profile URL: {json_file}")
        continue

    # Get the profile URL from the JSON data
    profile_url = data['Profile URL']

    # Make a request to the profile URL
    response = requests.get(profile_url)
    if response.status_code != 200:
        print(f"Failed to retrieve profile URL for JSON file: {json_file}")
        continue

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Get the profile URL from the response URL if not already obtained
    if 'Profile URL' not in data:
        data['Profile URL'] = response.url

    # Rename "Result URL" to "Profile URL" in the JSON data
    if 'Result URL' in data:
        data['Profile URL'] = data.pop('Result URL')

    # Update the JSON data with the scraped fields
    # Scrape the summary data
    summary_div = soup.find('div', id='summary')
    summary_span = summary_div.find('span') if summary_div else None
    data['Summary'] = summary_span.text.strip() if summary_span else 'blank'

    # Scrape the registration data
    registration_div = soup.find('div', id='registration')
    registration_span = registration_div.find('span') if registration_div else None
    data['Registration'] = registration_span.text.strip() if registration_span else 'blank'

    # Scrape the education data
    education_div = soup.find('div', class_='directory-profile__degree')
    data['Education'] = education_div.text.strip() if education_div else 'blank'

    # Scrape the contact data
    contact_div = soup.find('div', id='contact')
    contact_span = contact_div.find('span') if contact_div else None
    data['Contact'] = contact_span.text.strip() if contact_span else 'blank'

    # Save the updated JSON data back to the file
    with open(json_path, 'w') as file:
        json.dump(data, file, indent=4)

    print(f"Processed JSON file: {json_file}")

print("Data processing and JSON update complete.")
