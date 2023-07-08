import requests
from bs4 import BeautifulSoup

# Make an HTTP request to the website
url = 'https://catalog.mines.edu/coursesaz/'
response = requests.get(url)
html_content = response.content

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Find all the <a> tags in the parsed HTML
links = soup.find_all('a')

# Extract the href attribute from each <a> tag to get the link
departmentcodes = []
for link in links:
    href = link.get('href')
    if href!=None and '/coursesaz/' in href and href!='/coursesaz/' and href!='/coursesaz/coursesaz.pdf':
        departmentcodes.append(href)


