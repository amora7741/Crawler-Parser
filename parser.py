from bs4 import BeautifulSoup
from urllib.request import urlopen
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['crawlerDB']
pages = db['pages']

targetURL = pages.find_one({'url': 'https://www.cpp.edu/sci/computer-science/faculty-and-staff/permanent-faculty.shtml'})['url']
html = urlopen(targetURL)
soup = BeautifulSoup(html.read(), 'html.parser')

professorInfo = []
for div in soup.find_all("div", class_="clearfix"):
    professor = {}
    h2Tag = div.find('h2')

    if h2Tag:
        professor['name'] = h2Tag.get_text(strip=True)

    pTag = div.find('p')
    if pTag:
        for strongTag in pTag.find_all('strong'):
            key = strongTag.get_text(strip=True).replace(':', '').lower() #get info tags, remove colons
            
            if key in ['email', 'web']: #if on email or website tag, move to corresponding a tag
                aTag = strongTag.find_next('a')
                if aTag:
                    if key == 'email':
                        professor[key] = aTag.get_text(strip=True)
                    else:
                        professor[key] = aTag['href'] #get entire link including https

    if 'name' in professor:
        professorInfo.append(professor)

db['professors'].insert_many(professorInfo)

print("Faculty data inserted into MongoDB successfully.")