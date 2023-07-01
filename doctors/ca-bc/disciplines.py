import requests
from bs4 import BeautifulSoup
import os
import json
from datetime import datetime
import uuid

# Set up the base URL
url_base = 'https://www.cpsbc.ca/news/public-notifications?page='

# Specify the folder path for the current date
folder_path = os.path.join('scrapes', datetime.now().strftime('%Y-%m-%d'))

# Create the folder if it doesn't exist
os.makedirs(folder_path, exist_ok=True)

# Initialize a set to store unique URLs
existing_urls = set()

# Iterate over previous JSON files to collect existing URLs
for file in os.listdir(folder_path):
    if file.endswith('.json'):
        file_path = os.path.join(folder_path, file)
        with open(file_path) as json_file:
            data = json.load(json_file)
            existing_urls.add(data['URL'])

# Loop through the pages and export each row as a separate JSON file
for page_num in range(6):
    # Send an HTTP request to the webpage
    response = requests.get(url_base + str(page_num))
    # Parse the webpage content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    # Find the table that contains the disciplinary actions
    table = soup.find('table', {'class': 'table table-striped'})
    # Extract the data from the table and store it in a list
    rows = table.find_all('tr')
    for row in rows[1:]:
        cols = row.find_all('td')
        full_name = cols[0].find('a').text
        last_name, first_name = [name.strip() for name in full_name.split(',', 1)]
        url = cols[0].find('a')['href']
        date = cols[1].text.strip()

        # Check if the URL already exists in the existing data
        if url not in existing_urls:
            # Create a unique ID using UUID
            unique_id = str(uuid.uuid4())
            data = {'ID': unique_id, 'Last Name': last_name, 'First Name': first_name, 'URL': url, 'Date': date}

            # Specify the file path for the JSON file
            filepath = os.path.join(folder_path, f'{unique_id}.json')

            # Save the data as a JSON file
            with open(filepath, 'w') as json_file:
                json.dump(data, json_file, indent=4)

            # Add the URL to the existing URLs set
            existing_urls.add(url)

            print(f'Saved JSON file with ID: {unique_id}')
        else:
            print(f'Skipped URL: {url} (already exists)')
