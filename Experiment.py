import requests  # For making HTTP requests
from bs4 import BeautifulSoup  # For parsing HTML
from urllib.parse import urljoin, urlparse  # For URL manipulation
from whoosh import *
from flask import *
from flask import Flask, request, render_template


class Crawler:
    def __init__(self, start_url):
        self.start_url = start_url
        self.visited_links = set()
        self.index = {}

    def crawl(self, url):
        if url in self.visited_links:
            return

        self.visited_links.add(url)

        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
        except (requests.RequestException, ValueError):
            return

        if 'html' not in response.headers['content-type']:
            return

        soup = BeautifulSoup(response.text, 'html.parser')

        self.index_page(url, soup)

        links = soup.find_all('a')

        for link in links:
            href = link.get('href')

            if href:
                next_url = urljoin(url, href)

                if urlparse(next_url).netloc == urlparse(self.start_url).netloc:
                    self.crawl(next_url)

    def index_page(self, url, soup):
        words = soup.get_text().split()

        for word in words:
            if word not in self.index:
                self.index[word] = []

            self.index[word].append(url)

    def search(self, words):
        result_urls = set.intersection(*(set(self.index.get(word, [])) for word in words))

        return result_urls

    def print_index(self):
        return self.index

crawler = Crawler('https://vm009.rz.uos.de/crawl/index.html')
crawler.crawl(crawler.start_url)

search_results = crawler.search(['word1', 'word2'])
index = crawler.print_index()

from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser

schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)

from whoosh.index import create_in
import os
index_dir = "indexdir"
if not os.path.exists(index_dir):
    os.mkdir(index_dir)
ix = create_in(index_dir, schema)

writer = ix.writer()
for word, urls in crawler.index.items():
    for url in urls:
        writer.add_document(title=word, path=url, content=url)
writer.commit()

from whoosh.qparser import QueryParser
query_parser = QueryParser("title", ix.schema)
