# http://dict.baidu.com
# encoding=utf-8
import gzip
import linecache
import sys
import time
from http import cookiejar
from urllib import request, parse
from urllib.error import HTTPError

from bs4 import BeautifulSoup

path = '/data/txt/%s'
path = 'E:\\ts\\qidian\\%s'

url = "https://www.qidian.com/rank/fin?dateType=3&chn=21&page=%s"
filename = path % 'xuanhuan'

url = "https://www.qidian.com/rank/fin?dateType=3&chn=1&page=%s"
filename = path % 'qihuan'


def get_opener():
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                 'Chrome/64.0.3282.119 Safari/537.36 '
    head = [
        ('User-Agnet', user_agent),
        ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'),
        ('Accept-Encoding', 'gzip, deflate, br'),
        ('Accept-Language', 'zh-CN,zh;q=0.9'),
        ('Cache-Control', 'no-cache'),
        ('Host', 'www.qidian.com'),
        ('Upgrade-Insecure-Requests', '1'),
        ('Connection', 'keep-alive')
    ]
    cookie = cookiejar.CookieJar()
    cookie_support = request.HTTPCookieProcessor(cookie)
    _opener = request.build_opener(cookie_support)
    _opener.addheaders = head
    return _opener


def analyze():
    html = resp.read()
    html = html.decode('utf-8')
    html = BeautifulSoup(html, 'html.parser')
    rank = html.find("div", id="rank-view-list")
    if rank:
        for li in rank.select('li'):
            h4 = li.select("h4")[0]
            file.write(h4.text + ' ' + h4.select('a')[0].attrs['href'])
            file.write("\n")


if __name__ == '__main__':
    opener = get_opener()
    # request.install_opener(opener)

    file = open(filename, 'w', encoding='UTF-8')

    req = request.Request("https://www.qidian.com", method='GET')
    resp = opener.open(req)

    for index in range(1, 26):
        print(url % index)
        req = request.Request(url % index, method='GET')
        resp = opener.open(req)
        analyze()
    file.flush()
    file.close()
