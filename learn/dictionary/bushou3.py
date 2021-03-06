import gzip
import re
from http import cookiejar
from urllib import request

from bs4 import BeautifulSoup

countRe = re.compile('共 (\d+) 字')
path = "e:\\dict\\%s"

# src = path % 'cy-w.json'
# pur = path % 'cy.txt'

# src = path % 'z-w.json'
# pur = path % 'z.txt'
#
src = path % 'c-w.json'
pur = path % 'c.txt'

f = open(pur, 'w', encoding='UTF-8')


def read():
    bsf = open(src, 'r', encoding='UTF-8').readline()
    bushou1 = eval(bsf)
    return bushou1


def c(opener, url, f, word):
    has_next = True
    page = 1
    while has_next:
        has_next = False
        req_h = request.Request(url=url, headers=head, method='GET')
        response_h = opener.open(req_h)
        response_body = response_h.read()
        response_body = gzip.decompress(response_body)
        response_body = response_body.decode('utf-8')
        print(response_body)
        response_body = BeautifulSoup(response_body, 'html.parser')
        al = response_body.select('a')
        next_pn = 0
        for a in al:
            href = a.attrs['href']
            te = a.text
            if href == 'javascript:void(0);':
                if not te.isdigit():
                    continue
                if has_next:
                    continue
                next_pn = int(te)
                has_next = next_pn > page

            else:
                f.write("%s %s %s \n" % (te, href, word))

        page = next_pn
        url = url + "|" + str(page)


if __name__ == '__main__':
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                 'Chrome/64.0.3282.119 Safari/537.36 '
    head = {
        'User-Agnet': user_agent,
        'Accept': 'text/javascript, text/html, application/xml, text/xml, */*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Host': 'www.zdic.net',
        'Pragma': 'no-cache',
        'Referer': 'http://www.zdic.net/c/cybs/',
        'X-Prototype-Version': '1.5.0',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive'
    }
    cookie = cookiejar.CookieJar()
    cookie_support = request.HTTPCookieProcessor(cookie)
    opener = request.build_opener(cookie_support)
    req2 = request.Request(url="http://www.zdic.net/c/cybs/", headers=head, method='GET')
    res2 = opener.open(req2)
    bushou1 = read()
    total = 0
    for value in bushou1.values():
        if type(value) != dict:
            continue
        item = value['word']
        for bso in item:
            url = bso["href"]
            bs_url = url.replace('ci/', 'ci/sc/')
            c(opener, bs_url, f, bso['word'])
    f.flush()
    f.close()
