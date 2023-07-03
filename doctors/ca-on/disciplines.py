import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import uuid
import json

url = 'https://opsdt.ca/hearings/outcomes'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
table = soup.find('table', {'id': 'data-table'})

# Retrieve the data for each row in the table
rows = table.find_all('tr')

# Get the current date
current_date = datetime.now().strftime("%Y-%m-%d")

# Create the main subfolder using the current date
main_folder_path = f'scrapes/{current_date}'
os.makedirs(main_folder_path, exist_ok=True)

# Get the existing numerical subfolders
numerical_folders = [folder for folder in os.listdir(main_folder_path) if os.path.isdir(os.path.join(main_folder_path, folder))]

# Determine the next numerical folder
next_numerical_folder = str(int(numerical_folders[-1]) + 1).zfill(3) if numerical_folders else '001'

# Create the new numerical subfolder
numerical_folder_path = f'{main_folder_path}/{next_numerical_folder}'
os.makedirs(numerical_folder_path)

for row in rows:
    # Extract the data for the specified td tags with class names
    date = row.find('td', {'class': 'data-table__date'})
    if date is not None:
        date_str = date.text.strip()
        date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")
    else:
        date = ''

    name = row.find('td', {'class': 'data-table__name'})
    if name is not None:
        name = name.text.strip()
    else:
        name = ''

    file = row.find('td', {'class': 'data-table__file'})
    if file is not None:
        file = file.text.strip()
    else:
        file = ''

    details = row.find('td', {'class': 'data-table__details'})
    if details is not None:
        detail_divs = details.find_all('div', {'class': 'data-table__category'})
        details = ', '.join([div.text.strip() for div in detail_divs])
    else:
        details = ''

    links = row.find('td', {'class': 'data-table__links'})
    if links is not None:
        link_tags = links.find_all('a')
        doctor_link = link_tags[0]['href'] if len(link_tags) > 0 else ''
        other_links = [link['href'] for link in link_tags[1:]]
    else:
        doctor_link = ''
        other_links = []

    # Generate a random hash for the data ID
    data_id = str(uuid.uuid4())

    # Save the extracted data as a JSON file
    filename = data_id + '.json'
    data = {
        'Data ID': data_id,
        'Date': date,
        'Name': name,
        'File': file,
        'Details': details,
        'Profile URL': doctor_link,
        'Discipline URL': other_links
    }
    with open(f'{numerical_folder_path}/{filename}', 'w') as json_file:
        json.dump(data, json_file)

    # Print the extracted data
    print(f'Data ID: {data_id}\nDate: {date}\nName: {name}\nFile: {file}\nDetails: {details}\nProfile URL: {doctor_link}\nDiscipline URL: {other_links}\n')

print(f'Scraping data saved in: {numerical_folder_path}')