import requests
from bs4 import BeautifulSoup

# Send a GET request to the website
url = 'https://cpsnb.org/en/complaints/disciplinary-actions'
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find the <div> with itemprop="articleBody"
div_article_body = soup.find('div', itemprop='articleBody')

# Find all <p> elements with style="padding-left: 30px;" or style="padding-left: 2em;"
paragraphs = div_article_body.find_all('p', style=lambda value: value and (
            'padding-left: 30px;' in value or 'padding-left: 2em;' in value))

# Extract the desired information from each paragraph
for paragraph in paragraphs:
    name_span = paragraph.find('span', style='text-decoration: underline;')
    if name_span:
        name = name_span.text
    else:
        name = "Name not found"

    url_element = paragraph.find('a')
    if url_element:
        url = url_element['href']
    else:
        url = "URL not found"

    summary = paragraph.get_text(strip=True, separator=' ').replace(name, '').replace(url, '')

    print('Name:', name)
    print('URL:', url)
    print('Summary:', summary)
    print('---')
