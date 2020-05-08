# http://dict.baidu.com
# encoding=utf-8
import os
import time
import re
import string
import ssl
from http import cookiejar
from urllib import request,parse
from urllib.error import HTTPError

from bs4 import BeautifulSoup

path = '/house/19lou/village-%s.txt'
path = 'E:/house/19lou/village-%s.txt'

house_url = 'https://house.19lou.com/newhouse-house-%d&area=%d&name=&price=0&houseType=%d&homeType=%s'

house_types = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
areas_cn = ['上城区', '下城区', '西湖区', '江干区', '拱墅区', '滨江区', '萧山区', '余杭区', '富阳', '临安', '桐庐', '建德', '淳安', '钱塘新区']
areas = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
house_types_cn = ['公寓', '小高层', '高层', '排屋', '别墅', '商铺', '多层', '住宅', '商业', '办公', 'loft公寓', '沿街底商', '洋房', '叠墅', '院墅', '叠排','合院', '联排']
home_types_cn = ['一居室', '二居室', '三居室', '四居室', '五居室', '六居室', '复式室', '跃层']


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
    rank = html.find(".ss-result>ul>li")
    _page = html.find("div", attrs={"class": "hs-main-title"})
    _max = 26
    if _page:
        print (re.match("d",_page.text).grout(1))
    if rank:
        for li in rank:
            title = li.select("h2>a")[0]
            file.write(title + ' ' + title.attrs['href'])
            file.write("\n")
    max_page = 1


def refresh():
    cookie.clear()
    req_re = request.Request(url="https://house.19lou.com/newhouse", method='GET')
    opener.open(req_re)


if __name__ == '__main__':
    cookie = get_cookie()
    opener = get_opener()
    ssl._create_default_https_context = ssl._create_unverified_context

    now = time.strftime("%Y%m%d%H%M%S", time.localtime())
    filename = path % now
    file = open(filename, 'w', encoding='UTF-8')

    for area in areas:
        for house_type in house_types:
            for home_type in home_types_cn:
                home_type = parse.quote(home_type, safe=string.printable)
                isLastPage = False
                max_page = 1
                page = 1
                while not isLastPage:
                    url = house_url % (page, area, house_type, home_type)
                    print(url),
                    # try:
                    #     req = request.Request("https://house.19lou.com/newhouse-house-1&area=1&name=&price=0&houseType=1&homeType=%E4%B8%80%E5%B1%85%E5%AE%A4", method='GET', )
                    #     resp = opener.open(req)
                    #     analyze()
                    # except HTTPError as e:
                    #     print(e)
                    #     print(' fail'),
                    #     time.sleep(20)
                    #     count = 0
                    #     refresh()
                    #     continue
                    # print("")
                    page += 1
                    isLastPage = page > max_page