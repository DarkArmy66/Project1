AI & the Web Project 1 of 4
Project Title: Search Engine

Team Members
- Waldo Ungerer
- Mike Bediako Nsiah

The search engine will crawl and parse all HTML pages on a certain server that can be reached directly or indirectly from a start URL by following links on the pages

------------------
Components:

1. Crawler
2. Index
3. Query parser and search algorithm
4. User Frontend
-------------------------------------------------------------------------------

Project Plan:

X = done
? = in progress

[] Define the scope of the project.
[ ] Decide on the features of the search engine. (creativity +10)
[ ] Create a timeline for the project. (weekly breakdown)

-------------------------------------------------------------------------------------------------------

Week 1:
[x] Create Python environment (Python 3.10.0, MacBook Air, VS Code, Pyenv “V1”)
[x] Set up GitHub repo (each person to make own branch separate from main branch
[x] Add .gitignore and requirements.txt files
[x] Install “requests” and “BeautifulSoup” modules

---------------------------------------------------------------------------------------------------------------------------

[] Create a crawler.py file and define the skeleton of the crawling algorithm (build from pseudocode).
- Crawl (=get and parse) all HTML pages on a certain server
- that can directly or indirectly be reached from a start URL
- by following links on the pages.
- Do not follow links to URLs on other servers and only process HTML responses.
- Test the crawler with a simple website, e.g., https://vm009.rz.uos.de/crawl/index.html


[] Build an in-memory index from the HTML text content found (dictionary with words as keys and lists of URLs that refer to pages that include the word).

[] Add a function ‘search’ that takes a list of words as a parameter and returns (by using the index) a list of links to all pages that contain all the words from the list.

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

[] Debug and fix issues.

[] Improve efficiency and performance.

----------------------------------------------------------------


How to Contribute:
> Make your own branch separate from main branch.
> Finish code in your branch.
> Initiate pull request when ready.

----------------------------------------------------------------------------------------------------------------------------------------------------------------

End goal: Submit the code and the link to the demo deployment by due date (17/11).

Demonstrate it by crawling one website and making its content available to the user via a web frontend with a simple search form. 

Make the result available on the provided demo server.

Submit the code and the link to the demo deployment.