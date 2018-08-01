# http://dict.baidu.com
# encoding=utf-8
import gzip
import linecache
import sys
from http import cookiejar
from urllib import request, parse

from bs4 import BeautifulSoup

path = "e:\\dict\\%s"
src = path % 'z-h.txt'


def c(opener, item):
    print('dwomload %s %s' % (ln, item[0]), end='')
    item_data = {}
    w_url = url % parse.quote(item[0])
    req_h = request.Request(url=w_url, headers=head, method='GET')
    response_h = opener.open(req_h)
    response_body = response_h.read()
    response_body = gzip.decompress(response_body)
    response_body = response_body.decode('utf-8')
    html = BeautifulSoup(response_body, 'html.parser')

    head_info = html.find("div", id="word-header")
    basic = html.find("div", id="basicmean-wrapper")
    detail = html.find("div", id="detailmean-wrapper")
    table = html.find("div", id="table-info-wrapper")
    if head_info:
        lis = head_info.select("li")
        for li in lis:
            if li.attrs['id'] == 'tone_py':
                item_data[li.attrs['id']] = li.select("b")[0].text
                item_data["py_mp3"] = li.select("a")[0].attrs['url']
            else:
                item_data[li.attrs['id']] = li.select("span")[0].text

    if basic:
        lis = basic.select("li")
        means = []
        for li in lis:
            means.append(li.text)
        item_data["basic"] = means

    if detail:
        print(detail)

    if table:
        cels = table.select(".cell")
        info = {}
        for cel in cels:
            info[cel.attrs['id']] = cel.select("span")[0].text
        item_data["table"] = info

    return item_data


if __name__ == '__main__':
    ln = 0
    if len(sys.argv) == 1 or sys.argv[1] == '':
        ln = 1
    elif not str.isalnum(sys.argv[1]):
        sys.exit(9)
    else:
        ln = int(sys.argv[1])

    url = 'http://dict.baidu.com/s?wd=%s'
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                 'Chrome/64.0.3282.119 Safari/537.36 '

    head = {
        'User-Agnet': user_agent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Host': 'dict.baidu.com',
        'Upgrade-Insecure-Requests': '1',
        'Connection': 'keep-alive'
    }

    cookie = cookiejar.CookieJar()
    cookie_support = request.HTTPCookieProcessor(cookie)
    opener = request.build_opener(cookie_support)

    req2 = request.Request(url="http://dict.baidu.com", headers=head, method='GET')
    res2 = opener.open(req2)

    item = linecache.getline(src, ln)
    while item:
        item = item.strip().split(' ')
        c(opener, item)
        ln += 1
        item = linecache.getline(src, ln)
        sys.exit(0)
