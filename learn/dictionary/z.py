import gzip
import re
from http import cookiejar
from urllib import request, parse

from bs4 import BeautifulSoup

path = "e:\\dict\\%s"
pur = path % 'bushou1.json'
countRe = re.compile('共 (\d+) 字')

url = "http://www.zdic.net/z/jbs/bs/?bs=%s"
host = "http://www.zdic.net/z/jbs/"
src = path % 'z-w.txt'

f = open(src, 'w', encoding='UTF-8')


def read():
    bsf = open(pur, 'r', encoding='UTF-8').readline()
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
                if te == '':
                    te = '010'
                f.write("%s %s %s \n" % (te, href, word))
        page = next_pn
        url = url + "|" + str(page)
    f.flush()


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

    # f.writelines("--- %s" % url)
    # f.write("\n")

    bushou1 = read()
    for value in bushou1.values():
        if type(value) != list:
            continue
        for bso in value:
            bs = parse.quote(bso)
            bs_url = url % bs
            c(opener, bs_url, f, bso)
    f.flush()
    f.close()
