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

path = "e:\\dict\\%s"
# path = "/data/dict/%s"
src = path % 'z-h.txt'
tar = path % 'z-m.txt'


def c(opener, item_l):
    item_data = {'word': item_l[0]}
    w_url = url % parse.quote(item_l[0])
    global referer
    head['referer'] = referer
    print('dwomload %s %s' % (ln, w_url), end='')
    req_h = request.Request(url=w_url, headers=head, method='GET')
    response_h = opener.open(req_h)
    response_body = response_h.read()
    referer = w_url
    response_body = gzip.decompress(response_body)
    response_body = response_body.decode('utf-8')
    html = BeautifulSoup(response_body, 'html.parser')

    head_info = html.find("div", id="word-header")
    basic = html.find("div", id="basicmean-wrapper")
    detail = html.find("div", id="detailmean-wrapper")
    table = html.find("div", id="table-info-wrapper")
    if head_info:
        lis = head_info.select("li")
        li = lis[0]
        item_data[li.attrs['id']] = li.select("b")[0].text
        al = li.select("a")
        if len(al) > 1:
            item_data["py_mp3"] = li.select("a")[0].attrs['url']

        for i in range(1, len(lis)):
            li = lis[i]
            item_data[li.attrs['id']] = li.select("span")[0].text

    if basic:
        lis = basic.select("li")
        means = []
        for li in lis:
            means.append(li.text)
        item_data["basic"] = means

    if detail:
        dls = detail.select("dl")
        detail_info = {}
        for dl in dls:
            dts = dl.select("dt")
            if len(dts) == 1:
                detail_info[dts[0].text] = get_detail(dl)
            else:
                detail_info = get_detail(dl)
        item_data['detail'] = detail_info

    if table:
        cels = table.select(".cell")
        info = {}
        for cel in cels:
            info[cel.attrs['id']] = cel.select("span")[0].text
        item_data["table"] = info

    print(' success')
    return item_data


def get_detail(detail):
    details = detail.select("ol")
    titles = detail.select("strong")
    detail_means = {}
    for i in range(0, len(titles)):
        lis = details[i].select("li")
        class_meams = {}
        for li in lis:
            ps = li.select('p')
            if len(ps) > 0:
                ex = []
                for p in ps:
                    ex.append(p.text)
                class_meams[ps[0].text] = ex
        detail_means[titles[i].text.replace('〈', '').replace('〉', '')] = class_meams
    return detail_means


def refresh():
    cookie.clear()
    req_re = request.Request(url="http://dict.baidu.com/", headers=head, method='GET')
    opener.open(req_re)


if __name__ == '__main__':
    ln = 0
    if len(sys.argv) == 1 or sys.argv[1] == '':
        ln = 15320
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

    req2 = request.Request(url="http://dict.baidu.com/", headers=head, method='GET')
    res2 = opener.open(req2)

    item = linecache.getline(src, ln)
    f = open(tar, "a+", encoding='utf-8')
    referer = "http://dict.baidu.com/"
    count = 0
    while item:
        item_list = item.strip().split(' ')
        try:
            data = c(opener, item_list)
        except HTTPError as e:
            print(' fail')
            time.sleep(20)
            count = 0
            refresh()
            continue
        ln += 1
        f.write(str(data))
        f.write("\n")
        f.flush()
        item = linecache.getline(src, ln)
        time.sleep(0.3)
        count += 1
        if count == 50:
            count = 0
            refresh()
        # sys.exit(0)
    f.close()
