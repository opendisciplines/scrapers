import requests
import json
import os
from datetime import date
import uuid
from bs4 import BeautifulSoup

# Define the URL of the website
url = 'https://www.cps.sk.ca/imis/CPSS/Discipline/discipline.aspx?DisciplineCCO=Annual%20Discipline%20Summary'

# Send a GET request to the URL and store the response
response = requests.get(url)

# Create a Beautiful Soup object from the response content
soup = BeautifulSoup(response.content, 'html.parser')

# Find all the tables with class "rgMasterTable CaptionTextInvisible"
tables = soup.find_all('table', {'class': 'rgMasterTable CaptionTextInvisible'})

# Create a list to store the data for all the tables
data = []

# Set the starting index
index = 1

# Loop through the tables
for table in tables:
    # Find all the rows in the table
    rows = table.find_all('tr')

    # Loop through the rows and extract the data
    for row in rows:
        cells = row.find_all('td')
        if cells:
            url = f"https://www.cps.sk.ca{cells[0].find('a')['href']}"
            full_name = cells[0].text.strip()
            description = cells[1].text.strip()
            effective_date = cells[2].text.strip()
            outcome_date = cells[3].text.strip()
            hearing = cells[4].text.strip()
            try:
                decision = cells[5].text.strip()
            except IndexError:
                decision = ''

            # Check if hearing and decision are both present
            if hearing and decision:
                # Generate a unique hash code for the row
                data_id = str(uuid.uuid4())

                # Split the full name into last name and first name
                last_name, first_name = [name.strip().capitalize() for name in full_name.split(',')]

                # Add the row data to the list
                data.append({
                    'Data ID': data_id,
                    'Last Name': last_name,
                    'First Name': first_name,
                    'Profile URL': url,
                    'Category': description,
                    'Effective Date': effective_date,
                    'Outcome Date': outcome_date,
                    'Hearing': hearing,
                    'Decision': decision
                })
                print(
                    f'{data_id}, {last_name}, {first_name}, {description}, {effective_date}, {outcome_date}, {hearing}, {decision}')  # print the data to the console

# Create the "scrapes" directory if it doesn't exist
os.makedirs('scrapes', exist_ok=True)

# Get the current date
today = date.today().strftime('%Y-%m-%d')

# Create a subfolder with the current date if it doesn't exist
subfolder_path = f'scrapes/{today}'
os.makedirs(subfolder_path, exist_ok=True)

# Get the list of existing subfolders
existing_subfolders = sorted(os.listdir(subfolder_path))

# Increment the subfolder number
if existing_subfolders:
    last_subfolder = existing_subfolders[-1]
    subfolder_number = int(last_subfolder) + 1
else:
    subfolder_number = 1

# Generate the subfolder name with zero-padding
subfolder_name = str(subfolder_number).zfill(3)

# Create the final subfolder path
subfolder_path = os.path.join(subfolder_path, subfolder_name)

# Create the subfolder for the current scrape
os.makedirs(subfolder_path)

# Save each row of data as a separate JSON file
for row in data:
    data_id = row['Data ID']
    json_filename = os.path.join(subfolder_path, f'{data_id}.json')
    with open(json_filename, 'w') as json_file:
        json.dump(row, json_file)
