import gzip
import re
from http import cookiejar
from urllib import request

from bs4 import BeautifulSoup

countRe = re.compile('共 (\d+) 字')
path = "e:\\dict\\%s"

src = path % 'cy-w.json'
pur = path % 'cy.json'

# host = "http://www.zdic.net"
# src = 'z-w.json'
src = path % 'cy-w.json'
pur = path % 'cy.json'

src = path % 'c-w.json'
pur = path % 'c.json'

f = open(pur, 'w', encoding='UTF-8')


def read():
    bsf = open(src, 'r', encoding='UTF-8').readline()
    bushou1 = eval(bsf)
    return bushou1


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
    bushou2 = {}
    total = 0
    for value in bushou1.values():
        if type(value) != dict:
            continue
        item = value['word']
        for bso in item:
            url = bso["href"]
            bs_url = url.replace('ci/', 'ci/sc/')
            print(bs_url)
            req1 = request.Request(url=bs_url, headers=head, method='GET')
            response1 = opener.open(req1)
            html = response1.read()
            html = gzip.decompress(html)
            html = html.decode('utf-8')
            print(html)
            html = BeautifulSoup(html, 'html.parser')
            count = re.sub("\D", "", html.select("h2")[0].text)
            total = int(count) + total
            al = html.select('a')
            value = []
            for a in al:
                word = {}
                href = a.attrs['href']
                te = a.text
                word['href'] = href
                if te == '':
                    te = '010'
                word['word'] = te
                value.append(word)
            bushou2[bso["word"]] = {'count': count, 'word': value}

    bushou2["total"] = total
    print(total)
    f.write(str(bushou2))
    f.flush()
    f.close()
