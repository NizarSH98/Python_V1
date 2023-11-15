import requests
from bs4 import BeautifulSoup
import json

url = 'https://example.com'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Check if an <h1> element was found
title_element = soup.find('h1')
if title_element is not None:
    title = title_element.text
else:
    title = "No title found"

# Extract paragraphs
paragraphs = [p.text for p in soup.find_all('p')]

# Create the data dictionary
data = {
    'title': title,
    'paragraphs': paragraphs
}

# Write to JSON file
with open('output.json', 'w') as json_file:
    json.dump(data, json_file)
