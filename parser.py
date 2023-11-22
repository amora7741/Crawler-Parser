from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['crawlerDB']
pages = db['pages']

targetURL = pages.find_one({'url': 'https://www.cpp.edu/sci/computer-science/faculty-and-staff/permanent-faculty.shtml'})
html = targetURL['html']
soup = BeautifulSoup(html, 'html.parser')

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

            else: #all other information which does not contain an a tag
                value = strongTag.next_sibling

                if value:
                    professor[key] = value.get_text(strip=True)

    for k, v in professor.items():
        professor[k] = v.replace(':', '').strip()
    
    if 'name' in professor:
        professorInfo.append(professor)

db['professors'].insert_many(professorInfo)

print("Faculty data inserted into MongoDB successfully.")
print("fart")