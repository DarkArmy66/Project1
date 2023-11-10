# Import necessary libraries
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from whoosh.index import create_in
from whoosh.fields import *
import os
from whoosh.qparser import QueryParser
import shutil

# Define a Crawler class
class Crawler:
    def __init__(self, seed_url):
        # Initialize the crawler with the seed URL
        self.seed_url = seed_url
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

        # Print the indexed information
        for url, text_content in self.index.items():
            print(f"URL: {url}\nText Content: {text_content}\n")
            writer.add_document(title=url, content=text_content)

    def search(self, words):
        # Search the index for the given words
        result = []
        for url, text_content in self.index.items():
            if all(word in text_content for word in words):
                result.append(url)
        return result

# Create a new Crawler instance
crawler = Crawler('https://vm009.rz.uos.de/crawl/index.html')

# Define the schema for the index
schema = Schema(title=TEXT(stored=True), content=TEXT)

# The name of the directory to be deleted
index_dir = "indexdir"

# Get the current working directory
#cwd = os.getcwd()

# Create the full index directory path
index_dir_path = os.path.join(cwd, index_dir)

# Delete the directory if it exists
#if os.path.exists(index_dir_path):
    #shutil.rmtree(index_dir_path)

# Create the directory
#os.makedirs(index_dir_path)

# Now you can create the index in the new directory
ix = create_in(index_dir_path, schema)
writer = ix.writer()

# Start crawling
crawler.crawl()

# Commit the changes to the index
writer.commit()

# Search the index

# Get the search query from the user
search_query = input("Enter your search query: ")

with ix.searcher() as searcher:
    # Parse the user's search query
    query = QueryParser("content", ix.schema).parse(search_query)
    results = searcher.search(query)
    
    # Print all results
    for r in results:
        print(r)