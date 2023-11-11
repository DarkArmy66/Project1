# Import necessary libraries
from urllib.parse import urlparse, urljoin
import os
import socket
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
from whoosh.index import create_in, open_dir
from whoosh.fields import *

# Define a Crawler class
class Crawler:
    def __init__(self, seed_url, writer):
        # Initialize the crawler with the seed URL and the writer
        self.seed_url = seed_url
        self.writer = writer
        self.parsed_seed_url = urlparse(seed_url)
        self.visited_urls = set()
        self.urls_to_visit = set([seed_url])
        self.index = {}

    def crawl(self):
        # Crawl the web starting from the seed URL
        while self.urls_to_visit:
            url = self.urls_to_visit.pop()
            self.visited_urls.add(url)

            try:
                r = requests.get(url)
            except:
                continue

            soup = BeautifulSoup(r.content, 'html.parser')

            # Extract the text content of the page
            text_content = soup.get_text()

            # Clean up the HTML by removing unnecessary tags, scripts, etc.
            for script in soup(["script", "style"]):
                script.decompose()

            # Index the extracted information
            self.index[url] = text_content

            for tag in soup.find_all(True):
                if tag.has_attr('href'):
                    link = urljoin(url, tag['href'])  # Use urljoin to handle relative URLs
                    parsed_link = urlparse(link)

                    if parsed_link.netloc == self.parsed_seed_url.netloc and link not in self.visited_urls:
                        self.urls_to_visit.add(link)

        # Index the extracted information
        for url, text_content in self.index.items():
            self.writer.add_document(title=url, content=text_content)

    def search(self, words):
        # Search the index for the given words
        result = []
        for url, text_content in self.index.items():
            if all(word in text_content for word in words):
                result.append(url)
        return result

def setup_index():
    # Define the schema for the index, the name of the directory, get the current working directory, create the full index directory path
    schema = Schema(title=TEXT(stored=True), content=TEXT)
    index_dir = "indexdir"
    cwd = os.getcwd()
    index_dir_path = os.path.join(cwd, index_dir)

    # Check if the directory exists, open the existing index or create the directory and a new index in the directory
    if os.path.exists(index_dir_path):
        ix = open_dir(index_dir_path)
    else:
        os.makedirs(index_dir_path)
        ix = create_in(index_dir_path, schema)

    return ix.writer()

def setup_app(crawler):
    # Define Flask app, routes and functions
    app = Flask(__name__)

    @app.route('/', methods=['GET'])
    def home():
        return render_template('home.html')

    @app.route('/search', methods=['GET'])
    def search():
        query = request.args.get('q')
        results = crawler.search(query.split())
        return render_template('search.html', results=results)

    return app

def find_available_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))            # Bind to a free port provided by the host.
        return s.getsockname()[1]  # Return the port number assigned.

if __name__ == "__main__":
    writer = setup_index()
    crawler = Crawler('https://vm009.rz.uos.de/crawl/index.html', writer)
    crawler.crawl()
    writer.commit()
    app = setup_app(crawler)
    port = find_available_port()
    print(f"Running server on port {port}")
    app.run(debug=True, port=port)
