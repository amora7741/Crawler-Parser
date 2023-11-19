from urllib.request import urlopen
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['crawlerDB']
pages_collection = db['pages']