import requests
import time
import sys
import os
from pyquery import PyQuery as pq
from slugify import slugify
from datetime import datetime

search = "Game.of.Thrones.S06E08"
#search = "Prince Purple Rain mp3 by Aryong"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
}

r = requests.get('http://www.t411.ch/torrents/search/?name=%22{0}%22&'
                 'description=&file=&user=&cat=&search=%40name+%22{1}%22+&'
                 'submit=Recherche&order=added&type=desc&t={2}'
                 .format(search, search, time.time()), headers=headers)
d = pq(r.text)
g = d('.results a[title^="{0}"]'.format(search))
urls = [l.attrib['href'] for l in g]

if not len(urls):
    print('{0} Nothing found'.format(datetime.now()))


if len(urls):
    go_to = 'http:' + urls[0]
    
    rt = requests.get(go_to, headers=headers)
    dt = pq(rt.text)
    shortlink = dt('.shortlink')[0].attrib['href']
    short = slugify(shortlink, only_ascii=True)
    
    if os.path.exists(short + '.torrent') or os.path.exists(short + '.torrent.added'):
        print('{0} {1} already here'.format(datetime.now(), short))
        exit()
    
    s = requests.Session()
    rc = s.post('http://www.t411.ch/users/login/', {
        'login': sys.argv[1],
        'password': sys.argv[2],
    }, headers=headers)
    rt = s.get(go_to, headers=headers)
    dt = pq(rt.text)
    gt = dt('.accordion a[href^="/torrents/download/"]'.format(search))

    torrent_url = 'http://www.t411.ch' + gt[0].attrib['href']
    torrent = s.get(torrent_url, stream=True, headers=headers)

    with open(short + '.torrent', 'wb') as handle:
        for block in torrent.iter_content(1024):
            handle.write(block)
    print('{0} {1} downloaded'.format(datetime.now(), short))
