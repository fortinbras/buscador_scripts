# Import packages
import requests
from bs4 import BeautifulSoup

# Specify url
url = 'http://inep.gov.br/microdados'

# Package the request, send the request and catch the response: r
r = requests.get(url)

# Extracts the response as html: html_doc
html_doc = r.text

# create a BeautifulSoup object from the HTML: soup
soup = BeautifulSoup(html_doc, 'lxml')
soup.prettify()

all_hrefs = soup.find_all('a')
all_links = [link.get('href') for link in all_hrefs]

for link in all_links:
    if link and ('.zip' and 'superior') in link:
        print(link)

