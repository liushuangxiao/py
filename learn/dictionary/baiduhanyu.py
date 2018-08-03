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

# path = "F:\\data\\dict\\%s"
path = "/data/dict/%s"
path = 'e:\\dict\\%s'
src = path % 'c.txt'
tar = path % 'c-m.txt'
fail_file = path % 'c-m.fail.txt'


def c():
    item_data = {'word': item_list[0]}
    w_url = url % parse.quote(item_list[0])
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
    head_info = html.find("div", id="term-header")
    basic = html.find("div", id="basicmean-wrapper")
    detail = html.find("div", id="detailmean-wrapper")
    syn_ant = html.find("div", id="syn_ant_wrapper")
    baike = html.find("div", id="baike-wrapper")
    if head_info:
        bs = head_info.select("b")
        item_data['pinyin'] = bs[0].text
        al = head_info.select("a")
        if len(al) > 1:
            item_data["py_mp3"] = head_info.select("a")[0].attrs['url']

    if basic:
        means = {}
        for ol in basic.select("ol"):
            for li in ol.select("li"):
                ps = li.select('p')
                if len(ps) == 1:
                    means[ps[0].text] = '无例子'
                else:
                    means[ps[0].text] = ps[1].text
        item_data["basic"] = means

    if detail:
        ols = detail.select("ol")
        detail_means = {}
        for ol in ols:
            for li in ol.select("li"):
                ps = li.select('p')
                if len(ps) == 1:
                    detail_means[ps[0].text] = '无例子'
                else:
                    detail_means[ps[0].text] = ps[1].text
        item_data['detail'] = detail_means

    if syn_ant:
        synonym_elements = syn_ant.find("div", id="synonym")
        synonym_array = []
        if synonym_elements:
            for a in synonym_elements.select('a'):
                synonym_array.append(a.text)
        item_data['synonym'] = synonym_array

        antonym_elements = syn_ant.find("div", id="antonym")
        antonym_array = []
        if antonym_elements:
            for a in antonym_elements.select('a'):
                antonym_array.append(a.text)
        item_data['antonym'] = antonym_array

    if baike:
        baike_means = []
        for content in baike.select(".tab-content"):
            ps = content.select("p")
            al = content.select("a")
            for index in range(0, len(ps)):
                baike_item = {'baike': ps[index].text.replace('查看百科', "").strip(), 'href': al[index].attrs['href']}
                baike_means.append(baike_item)
        item_data['baike'] = baike_means

    print(' success')
    return item_data


def refresh():
    cookie.clear()
    req_re = request.Request(url="http://dict.baidu.com/", headers=head, method='GET')
    opener.open(req_re)


def fail():
    fail_w = open(fail_file, 'a+', encoding='utf-8')
    fail_w.write(str(item_list))
    fail_w.flush()
    fail_w.close()


if __name__ == '__main__':
    ln = 0
    if len(sys.argv) == 1 or sys.argv[1] == '':
        ln = 32865
    elif not str.isalnum(sys.argv[1]):
        sys.exit(9)
    else:
        ln = int(sys.argv[1])

    url = 'http://hanyu.baidu.com/s?wd=%s'
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

    req2 = request.Request(url="http://hanyu.baidu.com/", headers=head, method='GET')
    res2 = opener.open(req2)

    item = linecache.getline(src, ln)
    f = open(tar, "a+", encoding='utf-8')
    referer = "http://hanyu.baidu.com/"
    count = 0
    while item:
        item_list = item.strip().split(' ')
        try:
            data = c()
            f.write(str(data))
            f.write("\n")
            f.flush()
        except HTTPError as e:
            print(' fail')
            time.sleep(20)
            count = 0
            refresh()
            continue
        except IndexError as e:
            fail()
            print(' fail')
        ln += 1
        item = linecache.getline(src, ln)
        time.sleep(0.1)
        count += 1
        if count == 50:
            count = 0
            refresh()
    f.close()
