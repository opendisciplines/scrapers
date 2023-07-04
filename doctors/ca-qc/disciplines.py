import os
import requests
import json
import uuid
from bs4 import BeautifulSoup
from datetime import date

# Create the subfolder with the latest date
latest_date = date.today().strftime("%Y-%m-%d")
subfolder_path = f"scrapes/{latest_date}"
os.makedirs(subfolder_path, exist_ok=True)

# Loop through the years 2019 to 2023
index = 0
for year in range(2019, 2024):
    # Create the URL for the given year
    url = f"http://www.cmq.org/decisions-disciplinaires/index.aspx?lang=en&an={year}&mois=0#btSubmit"

    # Send a GET request to the URL and get the content
    response = requests.get(url)
    content = response.content

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(content, "html.parser")

    # Find the table with class "tableau1"
    table = soup.find("table", class_="tableau1")

    # Get all the rows of the table except the header row
    rows = table.find_all("tr")[1:]

    # Loop through the rows and write the data to individual JSON files
    for row in rows:
        # Get the columns of the row
        cols = row.find_all("td")

        # Get the data from the columns
        doc_name = cols[0].text.strip()
        case_file = cols[1].text.strip()
        decision_date = case_file[case_file.find("(") + 1 : case_file.find(")")]
        case_file = case_file[: case_file.find("(")].strip()
        decision_text = cols[2].text.strip()
        decision_url = cols[3].find("a")["href"]

        # Generate a UUID for the filename
        filename = str(uuid.uuid4())

        # Create a dictionary with the row data
        data = {
            "ID": filename,
            "Doctor Name": doc_name,
            "Case File": case_file,
            "Decision Date": decision_date,
            "Decision Text": decision_text,
            "Decision URL": decision_url,
        }

        # Write the data to a JSON file
        json_path = os.path.join(subfolder_path, f"{filename}.json")
        with open(json_path, "w") as json_file:
            json.dump(data, json_file, indent=4)

        # Increment the index counter
        index += 1

        # Print the data
        print(f"{filename}.json: {doc_name}, {case_file}, {decision_date}, {decision_text}, {decision_url}")
