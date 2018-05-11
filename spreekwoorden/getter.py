from urllib import request
from bs4 import BeautifulSoup
import json

url = 'https://spreekwoorden.nl/spreekwoorden-a-z'
pages = ['?page={}'.format(x) for x in range(1, 681)]

proverbs = dict()

for page in pages:
    html_page = request.urlopen(url + page).read()
    soup = BeautifulSoup(html_page, 'html.parser')
    html_proverbs = soup.find_all(attrs={'class': 'proverb-item'})
    for proverb in html_proverbs:
        title = proverb.find(attrs={'class': 'proverb-item__heading'}).text.strip()
        meaning = proverb.find(attrs={'class': 'proverb-item__body'}).text.strip()
        proverbs[title] = meaning

with open('dump.json', 'w') as f:
    json.dump(proverbs, f)
