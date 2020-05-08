# http://dict.baidu.com
# encoding=utf-8
import gzip
import os
import time
import re
import string
import ssl
import json
import math
import urllib.request
from http import cookiejar
from urllib import parse
from bs4 import BeautifulSoup

def getHtml(url):
    max_time = 5
    _time = 0
    print(url, end="")
    while _time < max_time:
        _time += 1
        time.sleep(0.4)
        try:
            page = urllib.request.urlopen(url)
            html = page.read()
            html = gzip.decompress(html)
            html = html.decode('utf-8', "ignore")
            # print(html)
            print(' success')
            return html
        except OSError as e:
            page = urllib.request.urlopen(url)
            html = page.read()
            html = html.decode('utf-8', "ignore")
            # print(html)
            print(' success')
            return html
        else:
            time.sleep(5)
            cookie.clear()
    print(' fail')
    return None


def postHtml(url, data):
    max_time = 5
    _time = 0
    print(url, end="")
    data = urllib.parse.urlencode(data).encode('utf-8')
    while _time < max_time:
        _time += 1
        time.sleep(0.4)
        try:
            page = urllib.request.urlopen(url, data=data)
            html = page.read()
            html = gzip.decompress(html)
            html = html.decode('utf-8', "ignore")
            # print(html)
            print(' success')
            return html
        except OSError as e:
            page = urllib.request.urlopen(url, data=data)
            html = page.read()
            html = html.decode('utf-8', "ignore")
            # print(html)
            print(' success')
            return html
        else:
            time.sleep(5)
            cookie.clear()
    print(' fail')
    return None


def getD(text):
    da = re.findall(r"[\d.]+", text)
    d = -1
    if (len(da) > 0):
        d = da[0]
    return str(d)


def getTotalPage(html, file):
    span = html.find("span", attrs={"class":"tips-num"})
    if not span:
        return 0;
    info = "## 共有 %d 实际导出 %d\n"
    total = float(span.text)
    pages = 0
    if total > 250 * 20:
        pages = 250
        info = info % (total, 250*20)
    else:
        pages = int(math.ceil(total/20.0))
        info = info % (total, total)
    file.write(info)
    return pages


cookie = cookiejar.CookieJar()
cookie_support = urllib.request.HTTPCookieProcessor(cookie)
ssl._create_default_https_context = ssl._create_unverified_context
opener = urllib.request.build_opener(cookie_support)
opener.addheaders = [
    ('User-Agent',
     'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'),
    ('host', 'www.tianyancha.com'),
    ('accept',
     'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'),
    ('accept-encoding', 'gzip, deflate, br'),
    ('accept-language', 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'),
    ('cache-control', 'max-age=0'),
    ('Connection', 'keep-alive'),
    ('cookie',
     'aliyungf_tc=AQAAAJsld2Yh7gIAgsd4ffnaI9ZrN2Vc; csrfToken=sg2cmYI8Pg4q-5a3o8iyHOB-; jsid=SEM-BAIDU-PZ2003-VI-000001; TYCID=709d0dd06f2711eab075e503b1874258; undefined=709d0dd06f2711eab075e503b1874258; ssuid=2051036100; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1585202577; _ga=GA1.2.1710480333.1585202577; _gid=GA1.2.1622942668.1585202577; RTYCID=fcd8d42a42464550a77461a7d296508a; CT_TYCID=8605fa7c59bc47619b8cd6acba283047; tyc-user-info=%257B%2522claimEditPoint%2522%253A%25220%2522%252C%2522vipToMonth%2522%253A%2522false%2522%252C%2522explainPoint%2522%253A%25220%2522%252C%2522integrity%2522%253A%252220%2525%2522%252C%2522state%2522%253A%25227%2522%252C%2522surday%2522%253A%25221093%2522%252C%2522announcementPoint%2522%253A%25220%2522%252C%2522schoolGid%2522%253A%2522%2522%252C%2522bidSubscribe%2522%253A%2522-1%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522monitorUnreadCount%2522%253A%25220%2522%252C%2522discussCommendCount%2522%253A%25220%2522%252C%2522onum%2522%253A%252213%2522%252C%2522claimPoint%2522%253A%25220%2522%252C%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNzc2NzE3NTU4NSIsImlhdCI6MTU4NTIwMzIyNSwiZXhwIjoxNjE2NzM5MjI1fQ.e_mPRHl4GdHXMVKdb4JegtBQWzscW9V1lJqW6N0xKX-icaodj_0jpilBzlximLE_pp0_0DhdAYU67JjzQqBjvg%2522%252C%2522schoolAuthStatus%2522%253A%25222%2522%252C%2522vipToTime%2522%253A%25221679631910005%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522companyAuthStatus%2522%253A%25222%2522%252C%2522myAnswerCount%2522%253A%25220%2522%252C%2522myQuestionCount%2522%253A%25220%2522%252C%2522signUp%2522%253A%25220%2522%252C%2522nickname%2522%253A%2522%25E8%25B1%25AA%25E9%25BC%258E%25E5%25AE%259E%25E4%25B8%259A%25E6%258A%2595%25E8%25B5%2584%2522%252C%2522privateMessagePointWeb%2522%253A%25220%2522%252C%2522privateMessagePoint%2522%253A%25220%2522%252C%2522isClaim%2522%253A%25220%2522%252C%2522educationBackground%2522%253A%2522%25E6%259C%25AC%25E7%25A7%2591%2522%252C%2522isExpired%2522%253A%25220%2522%252C%2522pleaseAnswerCount%2522%253A%25220%2522%252C%2522bizCardUnread%2522%253A%25220%2522%252C%2522vnum%2522%253A%252250%2522%252C%2522companyGid%2522%253A%2522%2522%252C%2522mobile%2522%253A%252217767175585%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNzc2NzE3NTU4NSIsImlhdCI6MTU4NTIwMzIyNSwiZXhwIjoxNjE2NzM5MjI1fQ.e_mPRHl4GdHXMVKdb4JegtBQWzscW9V1lJqW6N0xKX-icaodj_0jpilBzlximLE_pp0_0DhdAYU67JjzQqBjvg; tyc-user-phone=%255B%252217767175585%2522%255D; token=b4c1ef8e36ad48c48624aa389933de4c; _utm=47b59fbb81564cceb10b7cf1d8b8fb7d; cloud_token=57571065a0074dea84a98ad2f0a17e57; _gat_gtag_UA_123487620_1=1; bannerFlag=true; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1585207246'),
    ('referer', 'https://www.tianyancha.com/search?key=%E6%B2%B3%E5%B2%B8&base=zj'),
    ('sec-fetch-desc', 'document'),
    ('sec-fetch-mode', 'navigate'),
    ('sec-fetch-site', 'same-origin'),
    ('sec-fetch-user', '?1'),
    ('upgrade-insecure-requests', '1'),
]
urllib.request.install_opener(opener)

now = time.strftime("%Y%m%d", time.localtime())

prefix = "https://www.tianyancha.com"
upA = [
    ["https://www.tianyancha.com/search/os2?key=%E5%AE%A4%E5%86%85%E8%A3%85%E9%A5%B0&base=hangzhou", 'E:/720/tyc/snwzs.txt']
]
for up in upA:
    path = up[1]
    uri = up[0]
    file = open(path, 'w', encoding='UTF-8')

    html = getHtml(uri)
    # print(html)
    if not html:
        exit()
    html = BeautifulSoup(html, 'html.parser')
    pages = getTotalPage(html,file)
    itemDiv = html.find_all("div", attrs={"class":"sv-search-company"})
    info = "## %s   %d\n" % (uri ,len(itemDiv))
    file.write(info)
    file.flush()
    for div in itemDiv:
        a = div.find("a", attrs={"class":"name"})
        file.write(a.attrs["href"] + '\n')

    for page in range(2,pages+1):
        pUri = uri.replace('?', '/p' + str(page) + '?')
        html = getHtml(pUri)
        if not html:
            exit()
        html = BeautifulSoup(html, 'html.parser')
        itemDiv = html.find_all("div", attrs={"class":"sv-search-company"})
        info = "## %s   %d\n" % (uri ,len(itemDiv))
        file.write(info)
        for div in itemDiv:
            a = div.find("a", attrs={"class":"name"})
            file.write(a.attrs["href"] + '\n')
        file.flush()
    file.close()
