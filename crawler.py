from urllib.request import urlopen
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['crawlerDB']
pages = db['pages']

class Frontier:
    def __init__(self, initial_url):
        self.queue = [initial_url]
        self.visited = set()

    def addURL(self, url):
        if url not in self.visited and url not in self.queue:
            self.queue.append(url)

    def nextURL(self):
        if self.queue:
            url = self.queue.pop(0)
            self.visited.add(url)
            return url
        
        return None

    def done(self):
        return not self.queue
    
def retrieveURL(url):
    try:
        response = urlopen(url)
        html = response.read()
        return html
    except Exception as e:
        print(f"Error retrieving {url}: {e}")
        return None

def storePage(url, html):
    if html:
        pages.insert_one({'url': url, 'html': html})

def target_page(html):
    bs = BeautifulSoup(html, 'html.parser')
    
    headerTags = bs.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])

    for header in headerTags:
        if header.get_text() == "Permanent Faculty":
            return True
        
def parse(html, baseURL):
    bs = BeautifulSoup(html, 'html.parser')
    links = []

    for link in bs.find_all('a', href=True):
        href = link['href']
        fullURL = urljoin(baseURL, href)
        links.append(fullURL)

    return links

def crawlerThread(frontier):
    while not frontier.done():
        url = frontier.nextURL()
        if url:
            html = retrieveURL(url)
            bs = BeautifulSoup(html, 'html.parser')
            storePage(url, str(bs))

            if target_page(html):
                print(f"Target page found at {url}")
                frontier.queue = []
            else:
                newLinks = parse(html, url)
                for newURL in newLinks:
                    frontier.addURL(newURL)

    return False

if __name__ == "__main__":
    initialURL = 'https://www.cpp.edu/sci/computer-science/'
    frontier = Frontier(initialURL)
    crawlerThread(frontier)