import requests
from pyquery import PyQuery as pq

search = "Game.of.Thrones.S06E05"

r = requests.get('http://www.t411.ch/torrents/search/?name=%22Game.of.Thrones.S06E05%22&description=&file=&user=&cat=&search=%40name+%22Game.of.Thrones.S06E05%22+&submit=Recherche&order=added&type=desc')
d = pq(r.text)
g = d('.results a[title^="{0}"]'.format(search))

print(g)
