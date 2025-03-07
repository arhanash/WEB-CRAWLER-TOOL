import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs
import sqlite3
import os

def save_to_file(url, links, output_file='output.txt'):
    with open(output_file, 'w') as file:
        file.write(f"Crawled URL: {url}\n")
        file.write("=" * 60 + "\n")

        for full_url, params in links.items():
            file.write(f"URL: {full_url}\n")
            if params:
                file.write("Parameters:\n")
                for key, values in params.items():
                    file.write(f"  {key}: {', '.join(values)}\n")
            else:
                file.write("No parameters found\n")
            file.write("-" * 60 + "\n")
    print(f"Results saved to {os.path.abspath(output_file)}")


def save_to_database(url, links, db_file='crawl_results.db'):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS CrawledLinks
                      (id INTEGER PRIMARY KEY, url TEXT, parameter_key TEXT, parameter_value TEXT)''')

    for full_url, params in links.items():
        for key, values in params.items():
            for value in values:
                cursor.execute('''INSERT INTO CrawledLinks (url, parameter_key, parameter_value)
                                  VALUES (?, ?, ?)''', (full_url, key, value))

    conn.commit()
    conn.close()
    print(f"Results saved to database {os.path.abspath(db_file)}")


def crawl_and_extract_parameters(url, output_file='output.txt', db_file='crawl_results.db'):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        links = {}
        for link in soup.find_all('a', href=True):
            full_url = urljoin(url, link['href'])
            parsed_url = urlparse(full_url)
            params = parse_qs(parsed_url.query)
            links[full_url] = params

        save_to_file(url, links, output_file)
        save_to_database(url, links, db_file)

    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch the page: {e}")

# Run the crawler
url_to_crawl = 'https://upskill.teachnook.com/'  # Replace with the target URL
crawl_and_extract_parameters(url_to_crawl)
