import re
from urllib import request,error,parse
from http import cookiejar


if __name__ == '__main__':
    login_url = 'http://www.qishu.cc/xuanhuan/list1_1.html'
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'
    head = {'User-Agnet': user_agent, 'Connection': 'keep-alive'}
    data = {}
    data['a'] = '1'
    postData = parse.urlencode(data).encode('utf-8')
    cookie = cookiejar.CookieJar()
    cookie_support = request.HTTPCookieProcessor(cookie)
    opener = request.build_opener(cookie_support)

    req1 = request.Request(url=login_url, data=postData, headers=head,method='GET')
    response1 = opener.open(req1)
    html = response1.read()
    html = html.decode('GB18030')
    print(html)