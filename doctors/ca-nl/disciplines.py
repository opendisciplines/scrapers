import requests
from bs4 import BeautifulSoup

# Send a GET request to the website
url = "https://cpsnl.ca/complaints-discipline/discipline-hearings-and-settlement-agreements/"
response = requests.get(url)

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Find all tables with the specified class
tables = soup.find_all('table', class_='table1 table-striped')

# Specify the index of the desired table (e.g., if it's the second table, use tables[1])
desired_table = tables[1]

# Extract data from the table
data = []
for row in desired_table.find_all('tr'):
    row_data = []
    for cell in row.find_all('td'):
        cell_text = cell.text.strip()
        link = cell.find('a')
        if link:
            cell_text += " " + link['href']
        cell_text = cell_text.replace("Decision Summary", "").strip()
        if ',' in cell_text:
            last_name, first_name = cell_text.split(',', 1)
            last_name = last_name.strip().capitalize()
            row_data.extend([last_name, first_name.strip()])
        else:
            row_data.append(cell_text)
    if row_data:
        data.append(row_data)

# Print the extracted data
for row in data:
    print(row)
