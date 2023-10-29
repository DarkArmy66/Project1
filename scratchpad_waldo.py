from bs4 import BeautifulSoup

# An example HTML document
html_content = "<html><head><title>The Title</title></head><body>Body content.</body></html>"

# The BeautifulSoup class' constructor takes an HTML document as a string and a parser name
# We'll use the builtin 'html.parser'
soup = BeautifulSoup(html_content, 'html.parser')

# The soup object has a lot of attributes that correspond to HTML nodes (imagine the HTML document as a tree!)

title_tag = soup.title
print(title_tag)  # <title>The Title</title>

# get the text content of a Tag (including possibly nested subtags' content)
print(title_tag.text)

headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
for heading in headings:
    print(heading.text)