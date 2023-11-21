from bs4 import BeautifulSoup
from urllib.request import urlopen
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['crawlerDB']
pages = db['pages']