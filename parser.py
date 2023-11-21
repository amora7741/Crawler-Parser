from bs4 import BeautifulSoup
from urllib.request import urlopen
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['crawlerDB']
pages = db['pages']

targetURL = pages.find_one({'url': 'https://www.cpp.edu/sci/computer-science/faculty-and-staff/permanent-faculty.shtml'})['url']
html = urlopen(targetURL)
soup = BeautifulSoup(html.read(), 'html.parser')