import requests
from bs4 import BeautifulSoup

# Make a GET request to the website
url = 'https://www.cpspei.ca/disciplinary-decisions/'  # Replace with the actual URL
response = requests.get(url)

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Find all <article> elements with class "news_post"
articles = soup.find_all('article', class_='news_post')

# Iterate over the articles and extract the required data
for article in articles:
    # Extract the name from the <h3> tag
    name = article.find('h3').text.strip()

    # Get the part after the hyphen (if it exists)
    decision = name.split('- ', 1)[-1].strip()

    # Extract the URL from the <a> tag within the <p class="readmore">
    url = article.find('p', class_='readmore').find('a')['href']

    # Extract the summary text
    summary = article.text.strip().replace(name, '').replace(url, '').strip()

    # Print the extracted data
    print('Name:', decision)
    print('URL:', url)
    print('Summary:', summary)
    print('---')
