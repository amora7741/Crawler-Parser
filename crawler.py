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