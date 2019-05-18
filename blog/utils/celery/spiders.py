import os
import time

from bs4 import BeautifulSoup
import requests

from blog import celery

kgbook_url = 'https://www.kgbook.com'


def kgbook_search(name):
    return requests.post(
        url=kgbook_url + '/e/search/index.php',
        headers={
            'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0',
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Referer':
            'https://www.kgbook.com/waiguowenxue/1251.html'
        },
        cookies={'ecmslastsearchtime': str(int(time.time()))},
        data={
            'keyboard': name,
            'show': 'title, booksay, bookwriter',
            'tbname': 'download',
            'tempid': 1,
            'submit': '搜索',
        })


mybanshu_url = 'http://book.mybanshu.win'


def mybanshu(name):
    rep = requests.get(url=mybanshu_url + '/book/list', params={'kw': name})
    soup = BeautifulSoup(rep.text)
    contents = soup.select('div .content')
    result = []
    for content in contents:
        a = content.find['a']
        result.append({'name': a.string, 'url': mybanshu_url + a.get('href')})
    return result


bookset_url = 'https://bookset.me'


def bookset(name):
    result = []
    response = requests.get(bookset_url + '/search/' + name)
    soup = BeautifulSoup(response.text)
    items = soup.select('.card-item')
    for i in items:
        a_tags = i.select('a')
        if not a_tags[1].string or a_tags[-1].string == '-':
            continue
        result.append({
            'name': a_tags[1].string,
            'author': a_tags[-1].string,
            'url': a_tags[0].get('href')
        })
    return result

def get_bookset_download_url(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text)
    links = soup.select('.mbm-book-download-links-link')
    for link in links:
        if link.select('span')[0].string == 'mobi下载':
            return link.get('href')

def download(url, dest, name):
    path = os.path.join(dest, name)
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
