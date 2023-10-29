# Import the necessary libraries
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Define the Crawler class
class Crawler:
    # Initialize the crawler with the starting URL
    def __init__(self, start_url):
        self.start_url = start_url  # The URL to start crawling from
        self.visited_links = set()  # A set to store the URLs of the pages we've visited
        self.index = {}  # A dictionary to serve as our index, mapping words to URLs

    # Define the crawl method that will visit and parse pages
    def crawl(self, url):
        # If we've already visited this URL, we don't need to visit it again
        if url in self.visited_links:
            return

        # Add this URL to our set of visited links
        self.visited_links.add(url)

        # Try to send a GET request to the URL
        try:
            response = requests.get(url, timeout=5)  # We use a timeout of 5 seconds
            print(f"Status code for {url}: {response.status_code}")  # Print the status code
            response.raise_for_status()  # If the response contains an HTTP error status code (like 404), this line will raise an exception
        except (requests.RequestException, ValueError) as e:
            # If there was an error with the request (like a timeout, DNS resolution failure, etc.) or the URL was invalid, print an error message and return
            print(f"Unable to fetch page {url} due to {str(e)}")
            return

        # If the content type of the response is not HTML, we don't want to parse it
        if 'html' not in response.headers['content-type']:
            return

        # Parse the HTML content of the page with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Print out the parsed HTML content for debugging purposes
        print(soup.prettify())

        # Index this page (i.e., add its words to our index)
        self.index_page(url, soup)

        # Find all links on this page
        links = soup.find_all('a')

        # For each link...
        for link in links:
            href = link.get('href')  # Get the destination URL of the link

            # If this is a valid link...
            if href:
                next_url = urljoin(url, href)  # Construct an absolute URL from this relative URL
                
                # If this URL is on the same domain as our starting URL...
                if urlparse(next_url).netloc == urlparse(self.start_url).netloc:
                    self.crawl(next_url)  # ...crawl it!

    # Define a method that will add words from a page's text content to our index
    def index_page(self, url, soup):
        words = soup.get_text().split()  # Split the text content of the page into individual words
        
        # For each word...
        for word in words:
            if word not in self.index:  # If this word is not already in our index...
                self.index[word] = []  # ...initialize an empty list for it
            
            self.index[word].append(url)  # Add this URL to the list of URLs associated with this word

    # Define a method that will search our index for pages that contain all words in a given list
    def search(self, words):
        return set.intersection(*(set(self.index.get(word, [])) for word in words))  # This line returns all URLs that contain all given words

# Create a Crawler instance and start crawling!
crawler = Crawler('https://vm009.rz.uos.de/crawl/index.html')
crawler.crawl(crawler.start_url)

# Print out URLs containing your search words!
print(crawler.search(['word1', 'word2']))
