# Importing the required libraries
import requests  # For making HTTP requests
from bs4 import BeautifulSoup  # For parsing HTML
from urllib.parse import urljoin, urlparse  # For URL manipulation

# Defining the Crawler class
class Crawler:
    # Class constructor with the starting URL as a parameter
    def __init__(self, start_url):
        self.start_url = start_url  # Assigning the starting URL
        self.visited_links = set()  # Initializing a set to store visited URLs
        self.index = {}  # Initializing an empty dictionary for the index

    # Method to crawl the web page
    def crawl(self, url):
        if url in self.visited_links:  # If the URL has already been visited, return
            return

        self.visited_links.add(url)  # Add the URL to the set of visited links

        try:
            response = requests.get(url, timeout=5)  # Send a GET request to the URL with a timeout of 5 seconds
            print(f"Status code for {url}: {response.status_code}")  # Print the status code for debugging
            response.raise_for_status()  # Raise an exception if there's an HTTP error
        except (requests.RequestException, ValueError) as e:
            print(f"Unable to fetch page {url} due to {str(e)}")  # Print an error message if there's a request exception or value error
            return

        if 'html' not in response.headers['content-type']:  # If the content type is not HTML, return
            return

        soup = BeautifulSoup(response.text, 'html.parser')  # Parse the HTML content of the page

        print(soup.prettify())  # Print the parsed HTML content for debugging

        self.index_page(url, soup)  # Index the page

        links = soup.find_all('a')  # Find all links on the page

        for link in links:  # For each link on the page...
            href = link.get('href')  # Get the href attribute of the link

            if href:  # If there's an href attribute...
                next_url = urljoin(url, href)  # Construct an absolute URL from this relative URL

                if urlparse(next_url).netloc == urlparse(self.start_url).netloc:  # If this URL is on the same domain as our starting URL...
                    self.crawl(next_url)  # ...crawl it!

    def index_page(self, url, soup):
        words = soup.get_text().split()  # Split the text content into individual words

        print(f"Indexing {len(words)} words from {url}")  # Print a message indicating that this page is being indexed

        for word in words:  # For each word...
            if word not in self.index:  # If this word is not already in our index...
                self.index[word] = []  # ...initialize an empty list for it

            self.index[word].append(url)  # Add this URL to the list of URLs associated with this word

        print(f"Indexed {len(self.index)} unique words so far")  # Print a message indicating how many unique words have been indexed so far

    def search(self, words):
        print("WHAT ARE YOU LOOKING FOR?")
        result_urls = set.intersection(*(set(self.index.get(word, [])) for word in words))

        if result_urls:
            print("YOUR RESULTS:")
            for url in result_urls:
                print(url)
        else:
            print("NO RESULT, UPGRADE TO PREMIUM FOR A BETTER EXPERIENCE.")

    def print_index(self):
        for word, urls in self.index.items():  
            print(f"{word}: {urls}")  # Print each word and its associated URLs

# Create an instance of the Crawler class and start crawling!
crawler = Crawler('https://vm009.rz.uos.de/crawl/index.html')
crawler.crawl(crawler.start_url)

# Search for pages containing specified words and print out their URLs
crawler.search(['word1', 'word2'])

# Print out the entire index after all pages have been crawled.
crawler.print_index()

# User input box
user_input = input("Enter a word to search in the dictionary: ")
crawler.search([user_input])
