import os
import re
import time
from http import cookiejar
from urllib import request, parse

nameRe = re.compile('([^>]*) TXT全集下载<')
path = "e:\\ts\\%s"
src = path % 'name.txt'
if os.path.exists(src):
    os.rename(src, "%s.%s" % (src, time.strftime("%d-%m-%Y")))
f = open(src, 'w', encoding='UTF-8')


def get_names(data):
    global nameRe
    name_list = nameRe.findall(data)
    for name in name_list:
        global f
        name = name.split("/")
        for n in name:
            f.writelines(n)
            f.write("\n")


if __name__ == '__main__':
    url = "http://www.qishu.cc/xuanhuan/list1_%s.html"
    # url = "http://www.qishu.cc/yanqing/list2_%s.html"
    url = "http://www.qishu.cc/wuxia/list3_%s.html"
    url = "http://www.qishu.cc/danmei/list4_%s.html"
    url = "http://www.qishu.cc/kehuan/list6_%s.html"
    url = "http://www.qishu.cc/chuanyeu/list7_%s.html"
    url = "http://www.qishu.cc/wangyou/list8_%s.html"
    url = "http://www.qishu.cc/lishi/list9_%s.html"
    url = "http://www.qishu.cc/xiaoyuan/list5_%s.html"
    url = "http://www.qishu.cc/yanqing/list10_%s.html"
    url = "http://www.qishu.cc/wenxue/list11_%s.html"

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                 'Chrome/64.0.3282.119 Safari/537.36 '
    head = {'User-Agnet': user_agent, 'Connection': 'keep-alive'}
    data = {'a': '1'}
    postData = parse.urlencode(data).encode('utf-8')
    cookie = cookiejar.CookieJar()
    cookie_support = request.HTTPCookieProcessor(cookie)
    opener = request.build_opener(cookie_support)
    for i in range(1, 13):
        page = url % i
        f.writelines("--- %s" % page)
        print(page)
        f.write("\n")
        req1 = request.Request(url=page, data=postData, headers=head, method='GET')
        response1 = opener.open(req1)
        html = response1.read()
        # print(html)
        html = html.decode('GB18030')
        get_names(html)
        f.flush()
    f.close()
