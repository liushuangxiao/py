import re
from http import cookiejar
from urllib import request, parse

from bs4 import BeautifulSoup

nameRe = re.compile('([^>]*) TXT全集下载<')
url = "http://www.zdic.net/z/jbs/"
# url = "http://www.zdic.net/c/cibs/"
src = 'bushou1.json'
f = open(src, 'w', encoding='UTF-8')


if __name__ == '__main__':
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                 'Chrome/64.0.3282.119 Safari/537.36 '
    head = {'User-Agnet': user_agent, 'Connection': 'keep-alive'}
    data = {}
    postData = parse.urlencode(data).encode('utf-8')
    cookie = cookiejar.CookieJar()
    cookie_support = request.HTTPCookieProcessor(cookie)
    opener = request.build_opener(cookie_support)
    # f.writelines("--- %s" % url)
    # f.write("\n")
    print(url)
    req1 = request.Request(url=url, data=postData, headers=head, method='GET')
    response1 = opener.open(req1)
    html = response1.read()
    html = html.decode('utf-8')
    html = BeautifulSoup(html, 'html.parser')
    table = html.select("table")
    trs = table[0].select("tr")
    cdata = {}
    total = 0
    for tr in trs:
        title = tr.select('.bsyx')
        if len(title) == 0:
            continue
        key = title[0].text;
        value = []
        al = tr.select('a')
        for a in al:
            total += 1
            value.append(a.text)
        cdata[key] = value
    cdata['total'] = total
    print(total)
    f.write(str(cdata))
    f.flush()
    f.close()
