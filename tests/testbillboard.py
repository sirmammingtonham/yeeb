from bs4 import BeautifulSoup
import requests
import json

url = 'https://www.billboard.com/charts/hot-100'

r=requests.get(url)

soup = BeautifulSoup(r.text, 'html.parser')

div = soup.find('div', {'class': 'chart-list chart-details__left-rail'})

songs = div.attrs['data-video-playlist']

songs_list = json.loads(songs)

print([x["title"] for x in songs_list])

