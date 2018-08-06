# http://dict.baidu.com
# encoding=utf-8
import os
import time
from http import cookiejar
from urllib import request
from urllib.error import HTTPError

from bs4 import BeautifulSoup

path = '/data/txt/%s/'
path = 'E:\\ts\\qidian\\%s\\'
path = 'F:\\data\\book\\qidian\\%s\\'

url_finish = ["https://www.qidian.com/rank/fin?style=1&dateType=2&chn=21&page=%s",
              "https://www.qidian.com/rank/fin?style=1&dateType=2&chn=1&page=%s",
              "https://www.qidian.com/rank/fin?style=1&dateType=2&chn=2&page=%s",
              "https://www.qidian.com/rank/fin?style=1&dateType=2&chn=22&page=%s",
              "https://www.qidian.com/rank/fin?style=1&dateType=2&chn=4&page=%s",
              "https://www.qidian.com/rank/fin?style=1&dateType=2&chn=15&page=%s",
              "https://www.qidian.com/rank/fin?style=1&dateType=2&chn=6&page=%s",
              "https://www.qidian.com/rank/fin?style=1&dateType=2&chn=5&page=%s",
              "https://www.qidian.com/rank/fin?style=1&dateType=2&chn=7&page=%s",
              "https://www.qidian.com/rank/fin?style=1&dateType=2&chn=8&page=%s",
              "https://www.qidian.com/rank/fin?style=1&dateType=2&chn=9&page=%s",
              "https://www.qidian.com/rank/fin?style=1&dateType=2&chn=10&page=%s",
              "https://www.qidian.com/rank/fin?style=1&dateType=2&chn=12&page=%s"
              ]

url_recom = ["https://www.qidian.com/rank/recom?style=1&dateType=2&chn=21&page=%s",
             "https://www.qidian.com/rank/recom?style=1&dateType=2&chn=1&page=%s",
             "https://www.qidian.com/rank/recom?style=1&dateType=2&chn=2&page=%s",
             "https://www.qidian.com/rank/recom?style=1&dateType=2&chn=22&page=%s",
             "https://www.qidian.com/rank/recom?style=1&dateType=2&chn=4&page=%s",
             "https://www.qidian.com/rank/recom?style=1&dateType=2&chn=15&page=%s",
             "https://www.qidian.com/rank/recom?style=1&dateType=2&chn=6&page=%s",
             "https://www.qidian.com/rank/recom?style=1&dateType=2&chn=5&page=%s",
             "https://www.qidian.com/rank/recom?style=1&dateType=2&chn=7&page=%s",
             "https://www.qidian.com/rank/recom?style=1&dateType=2&chn=8&page=%s",
             "https://www.qidian.com/rank/recom?style=1&dateType=2&chn=9&page=%s",
             "https://www.qidian.com/rank/recom?style=1&dateType=2&chn=10&page=%s",
             "https://www.qidian.com/rank/recom?style=1&dateType=2&chn=12&page=%s"
             ]
filenames = ['xuanhuan',
             'qihuan',
             'wuxia',
             'xianxia',
             'dushi',
             'xianshi',
             'junshi',
             'lishi',
             'youxi',
             'tiyu',
             'kehuan',
             'lingyi',
             'erciyuan'
             ]

datas = [
    {'urls': url_finish, 'filenames': filenames, 'path': 'wanben'},
    {'urls': url_recom, 'filenames': filenames, 'path': 'recom'},
]


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

    cookie_support = request.HTTPCookieProcessor(cookie)
    _opener = request.build_opener(cookie_support)
    _opener.addheaders = head
    return _opener


def get_cookie():
    return cookiejar.CookieJar()


def analyze():
    html = resp.read()
    html = html.decode('utf-8')
    html = BeautifulSoup(html, 'html.parser')
    rank = html.find("div", id="rank-view-list")
    page = html.find("div", id="page-container")
    _max = 26
    if page:
        _max = page.attrs['data-pagemax']
    if rank:
        for li in rank.select('li'):
            h4 = li.select("h4")[0]
            file.write(h4.text + ' ' + h4.select('a')[0].attrs['href'])
            file.write("\n")
    return _max


def refresh():
    cookie.clear()
    req_re = request.Request(url="http://dict.baidu.com/", method='GET')
    opener.open(req_re)


if __name__ == '__main__':

    cookie = get_cookie()
    opener = get_opener()
    # request.install_opener(opener)

    for di in range(0, len(datas)):
        data = datas[di]
        urls = data['urls']
        _file_names = data['filenames']

        dp = path % data['path']
        if not os.path.exists(dp):
            os.makedirs(dp)

        for i in range(0, len(urls)):
            filename = dp + _file_names[i]
            url = urls[i]

            file = open(filename, 'w', encoding='UTF-8')
            req = request.Request("https://www.qidian.com", method='GET')
            resp = opener.open(req)

            index = 1
            while index < 26:
                print("%s %s " % (di, i), end='')

                try:
                    print(url % index, end='')
                    req = request.Request(url % index, method='GET')
                    resp = opener.open(req)
                    max_page = analyze()
                    print(' success')
                    if index == int(max_page):
                        break
                except HTTPError as e:
                    print(' fail')
                    time.sleep(20)
                    count = 0
                    refresh()
                    continue
                index += 1
                time.sleep(0.2)

            index = 1
            file.flush()
            file.close()
            refresh()
