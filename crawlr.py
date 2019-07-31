import requests
from lxml import html
import re
from urllib.parse import urlparse, urljoin
import json

base_url = r'https://www.georgetown.edu'

to_crawl = [base_url]
complete = []
blacklist = []
data = {}
fails = []
lens_tc = []
lens_com = []


def get_urls(body):
    urls = []
    for x in body.xpath('//a'):
        url = None
        sub_url = x.get('href')
        if sub_url is not None and sub_url.startswith('/'):
            url = urljoin(base_url, sub_url)
        elif sub_url is not None and sub_url.startswith('http'):
            m = re.search('htt.*//.*\.georgetown.edu', sub_url)
            if m:
                url = sub_url
        if url is not None and url.endswith('/'):
            url = url[:-1]
        urls.append(url)
    return urls 

def gettr(url):
    try:
        r = requests.get(u)
        dta = {'content': r.text, 'urls': [], 'status': r.status_code}
        sc = r.status_code
    except:
        r = None
        sc = 'error'
        dta = {'content': 'error', 'urls': [], 'status': 'error'}

    if sc == 200 or sc == 'error':
        print('[{}] --'.format(sc), u)

    return r, sc, dta

i = 0
while len(to_crawl) > 0:# and i < 250:
    #i += 1
    u = to_crawl.pop()
    complete.append(u)
    
    r, sc, dta = gettr(u)
    data[u] = dta 
    
    if r is not None and sc == 200:
        body = html.fromstring(r.content)

        urls = [url for url in get_urls(body) if url is not None and url not in to_crawl and url not in complete]
        to_crawl += list(set(urls))
        data[u]['urls'] += urls

        lens_tc.append(len(to_crawl))
        lens_com.append(len(complete))



full_data = {'to_crawl': to_crawl, 
             'complete': complete,
             'data': data,
             'fails': fails,
             'to_crawl_lens': lens_tc,
             'complete_lens': lens_com 
}

js = json.dumps(full_data)
with open('crawling_data.json', 'w') as fout:
    fout.write(js)
