The search engine will crawl and parse all HTML pages on a certain server that can be reached directly or indirectly from a start URL by following links on the pages

------------------
Components:

1. Crawler
2. Index
3. Query parser and search algorithm
4. User Frontend

[] Create a crawler.py file and define the skeleton of the crawling algorithm (build from pseudocode).
- Crawl (=get and parse) all HTML pages on a certain server
- that can directly or indirectly be reached from a start URL
- by following links on the pages.
- Do not follow links to URLs on other servers and only process HTML responses.
- Test the crawler with a simple website, e.g., https://vm009.rz.uos.de/crawl/index.html


[] Build an in-memory index from the HTML text content found (dictionary with words as keys and lists of URLs that refer to pages that include the word).

[] Add a function ‘search’ that takes a list of words as a parameter and returns (by using the index) a list of links to all pages that contain all the words from the list.

Replace the simple index with code using the woosh library ( will be introduced in week 3 - https://whoosh.readthedocs.io/en/latest/intro.html ).
Build a flask app (will be introduced in week 3 - ) with two URLs that shows the following behaviour:
GET home URL: Show search form
GET search URL with parameter q: Search for q using the index and display a list of URLs as links


Improve the index by adding information (ideas will be presented in week 4)
Improve the output by including title and teaser text
Install your search engine on the demo server provided (will be introduced in week 4)

End goal: Submit the code and the link to the demo deployment by due date (17/11).

Demonstrate it by crawling one website and making its content available to the user via a web frontend with a simple search form. 

Make the result available on the provided demo server.

Submit the code and the link to the demo deployment.