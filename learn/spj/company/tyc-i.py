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
    da = re.findall(r"[\d.\+]+", text)
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
    ('upgrade-insecure-requests', '1'),
]
urllib.request.install_opener(opener)

now = time.strftime("%Y%m%d", time.localtime())
path = "E:/720/tyc/company.txt"
file = open(path, 'w', encoding='UTF-8')

prefix = "https://www.tianyancha.com"
upA = [
    'E:/720/tyc/snwzs.txt'
]
for up in upA:
    itemFile = open(up, 'r', encoding='UTF-8')
    cout = 0
    for line in itemFile:
        line = line.strip()
        if line.startswith('## '):
            continue
        html = getHtml(line)
        # print(html)
        if not html:
            exit()
        itemDict = {}
        html = BeautifulSoup(html, 'html.parser')
        detail = html.find("div",attrs={"class":"detail"})
        if not detail:
            cookie.clear()
            file.write(line)
            file.write("\n")
            # break
            continue
        detailItems = detail.find_all("div",attrs={"class":"in-block"})
        for di in detailItems:
            sp = di.contents
            itemDict[sp[0].text.strip()] = sp[1].text.strip()

        summary = detail.find("div", attrs={"class":"summary"})
        summarySp = summary.select("span")
        itemDict[summarySp[0].text.strip()] = summarySp[1].text.strip()
        humancompany = html.find("div",attrs={"class":"humancompany"}).find("a")
        itemDict["法定代表人"] = humancompany.attrs["title"]

        table = html.find("div",attrs={"id":"_container_baseInfo"}).select("table")[1]
        trs = table.find_all("tr")
        for tr in trs:
            tds = tr.select("td")
            tdl = len(tds)
            itemDict[tds[0].text.strip()] = tds[1].text.strip()
            if tdl > 3:
                itemDict[tds[2].text.strip()] = tds[3].text.strip()
            if tdl > 4:
                itemDict["评分"] = getD(tds[4].text.strip())
        file.write(json.dumps(itemDict))
        file.write("\n")
        if cout > 200:
            file.flush()
            cout = 0
    file.flush()
    itemFile.close()
file.close()
