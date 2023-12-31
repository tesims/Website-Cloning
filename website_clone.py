# -*- coding: utf-8 -*-
"""website-clone.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UfzzvG53HvfY4Tl_VCfWXtXpC85X_-_H
"""

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def scrape_website(url):
    # Create a session to handle cookies
    session = requests.Session()

    # Send a GET request to the URL
    response = session.get(url)
    response.raise_for_status()

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Create a directory for the website files
    parsed_url = urlparse(url)
    base_dir = parsed_url.netloc
    os.makedirs(base_dir, exist_ok=True)

    # Clone HTML file
    html_filename = os.path.join(base_dir, 'index.html')
    with open(html_filename, 'w', encoding='utf-8') as html_file:
        html_file.write(response.text)

    # Clone CSS files
    css_files = soup.find_all('link', {'rel': 'stylesheet'})
    for css in css_files:
        css_url = urljoin(url, css['href'])
        css_filename = os.path.join(base_dir, os.path.basename(css_url))
        response = session.get(css_url)
        response.raise_for_status()
        with open(css_filename, 'w', encoding='utf-8') as css_file:
            css_file.write(response.text)

    # Clone JS files
    js_files = soup.find_all('script', {'src': True})
    for js in js_files:
        js_url = urljoin(url, js['src'])
        js_filename = os.path.join(base_dir, os.path.basename(js_url))
        response = session.get(js_url)
        response.raise_for_status()
        with open(js_filename, 'w', encoding='utf-8') as js_file:
            js_file.write(response.text)

    print("Website cloned successfully!")

# Example usage
url = "https://www.youtube.com/results?search_query=AI+agent"
scrape_website(url)