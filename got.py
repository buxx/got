import requests
import time
import sys
from pyquery import PyQuery as pq

search = "Game.of.Thrones.S06E05"

r = requests.get('http://www.t411.ch/torrents/search/?name=%22{0}%22&'
                 'description=&file=&user=&cat=&search=%40name+%22{1}%22+&'
                 'submit=Recherche&order=added&type=desc&t={2}'
                 .format(search, search, time.time()))
d = pq(r.text)
g = d('.results a[title^="{0}"]'.format(search))
urls = [l.attrib['href'] for l in g]


if len(urls):
    go_to = 'http:' + urls[0]
    s = requests.Session()
    rc = s.post('http://www.t411.ch/users/login/', {
        'login': sys.argv[1],
        'password': sys.argv[2],
    })
    rt = s.get(go_to)
    dt = pq(rt.text)
    gt = dt('.accordion a[href^="/torrents/download/"]'.format(search))
    torrent_url = 'http://www.t411.ch' + gt[0].attrib['href']

    torrent = s.get(torrent_url, stream=True)

    with open('output.jpg', 'wb') as handle:
        for block in torrent.iter_content(1024):
            handle.write(block)
