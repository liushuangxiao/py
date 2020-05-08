# http://dict.baidu.com
# encoding=utf-8
import gzip
import os
import time
import re
import string
import ssl
import json
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


def getGoodsPrice(html):
    matchObj = re.search(r'goods_list =(.+);', html)
    if matchObj:
        return json.loads(matchObj.group(1))
    return {}


def getProperties(html):
    lis = html.select("li")
    properties = {}
    for li in lis:
        attr = li.select("span")
        key = attr[0].text.replace("：","")
        value = attr[1].text.replace("\\","/").replace("\t","")
        properties[key] = value
    return properties


def getId(uri):
    matchObj = re.search(r'/goods/(\d+)/', uri)
    if matchObj:
        return matchObj.group(1)
    return None


def getIntroImage(id):
    html = postHtml(introImageUri, {"item_id": id})
    images = []
    if not html:
        return images
    html = BeautifulSoup(html, 'html.parser')
    imgs = html.find_all("img")
    for img in imgs:
        images.append(img.attrs["data-src"])
    return images


def getSetImage(html):
    imgs = html.find_all("img", attrs={"class":"sp-image"})
    images = []
    for img in imgs:
        images.append(img.attrs["src"])
    return images


def toItemArray(itemsHtml):
    items = []
    for itemHtml in itemsHtml:
        items.append(itemHtml.attrs["href"])
    return items


cookie = cookiejar.CookieJar()
cookie_support = urllib.request.HTTPCookieProcessor(cookie)
ssl._create_default_https_context = ssl._create_unverified_context
opener = urllib.request.build_opener(cookie_support)
opener.addheaders = [
    ('User-Agent',
     'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'),
    ('authority', 'www.jiazhuangpei.com'),
    ('method', 'GET'),
    ('path', '/combo/detail?id=109'),
    ('scheme', 'https'),
    ('path', '/combo/detail?id=109'),
    ('accept',
     'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'),
    ('accept-encoding', 'gzip, deflate, br'),
    ('accept-language', 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'),
    ('cache-control', 'max-age=0'),
    ('cookie',
     'NTKF_T2D_CLIENTID=guestAD45CAEB-23D7-98FA-63CA-7F3FDFBAE13E; PHPSESSID=8b981e7f67cd4e7202a6e0503b1c6cc1; SERVERID=276a4c00a3911cb99ff5f8f9680ce2e8|1583825101|1583824811'),
    ('referer', 'https://partner.jiazhuangpei.com/combo/v2018_combo_list?style=0&kw='),
    ('sec-fetch-mode', 'navigate'),
    ('sec-fetch-site', 'same-site'),
    ('sec-fetch-user', '?1'),
    ('upgrade-insecure-requests', '1'),
]
urllib.request.install_opener(opener)

now = time.strftime("%Y%m%d", time.localtime())

# 套餐uri
# uri = "https://www.jiazhuangpei.com/combo/detail?id=273"
# path = 'E:/720/jiazhuangpei/93.txt'
# uri = "https://www.jiazhuangpei.com/combo/detail?id=272"
# path = 'E:/720/jiazhuangpei/92.txt'
# uri = "https://www.jiazhuangpei.com/combo/detail?id=237"
# path = 'E:/720/jiazhuangpei/83.txt'
# uri = "https://www.jiazhuangpei.com/combo/detail?id=109"
# path = 'E:/720/jiazhuangpei/37.txt'
# uri = "https://www.jiazhuangpei.com/combo/detail?id=1"
# path = 'E:/720/jiazhuangpei/01.txt'

prefix = "https://www.jiazhuangpei.com"
introImageUri = "https://www.jiazhuangpei.com/index.php/goods/get_item_desc"
upA = [
        ["https://www.jiazhuangpei.com/combo/detail?id=273", 'E:/720/jiazhuangpei/93.txt']
        ,["https://www.jiazhuangpei.com/combo/detail?id=272", 'E:/720/jiazhuangpei/92.txt']
        ,["https://www.jiazhuangpei.com/combo/detail?id=237", 'E:/720/jiazhuangpei/83.txt']
        ,["https://www.jiazhuangpei.com/combo/detail?id=109", 'E:/720/jiazhuangpei/37.txt']
        ,["https://www.jiazhuangpei.com/combo/detail?id=1", 'E:/720/jiazhuangpei/01.txt']
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
    setDict = {}

    mainItemAs = html.find("div",attrs={"class": "jd_carousel"}).find_all("a", attrs={"class": "sale_class"})
    mainItemAs = toItemArray(mainItemAs)
    setDict["mainItem"] = mainItemAs

    itemAs = html.find_all("a", attrs={"class": "sale_class"})
    images = getSetImage(html.find("div", attrs={"class": "sp-slides"}))
    setDict["image"] = images

    setDict["introImage"] = html.find("div", attrs={"class": "item_desc"}).find("img").attrs["src"]

    for itemA in itemAs:
        itemDict = {}
        # buy info
        buyinfo = itemA.parent.find("div", attrs={"class": "buy_info"})
        choose = buyinfo.select("div")[0].text.strip() + '_' + buyinfo.select("div")[1].text.strip()
        itemDict["choose"]=choose
        # buy num
        buyNum = itemA.parent.find("input", attrs={"class": "buy_num"})

        url = prefix + itemA.attrs["href"]
        id = getId(url)
        detail_html = getHtml(url)
        # print(detail_html)
        if not detail_html:
            print("跳过了 %s" % url)
            continue
        # 从js中获取到 价格对应字典
        price = getGoodsPrice(detail_html)
        itemDict["price"] = price
        # html 解析
        detail_html = BeautifulSoup(detail_html, 'html.parser')
        # item name
        nameDiv = detail_html.find("div", attrs={"class":"top_r"})
        if not nameDiv:
            nameDiv = detail_html.find("div", attrs={"class":"intro_top"})
        name = nameDiv.find("h3")
        itemDict["name"] = name.text
        # item image
        item_responsive_list = detail_html.find_all("li", attrs={"class": "item responsive"})
        images = []
        for item_responsive in item_responsive_list:
            item_url = item_responsive.find("img").attrs['src']
            images.append(item_url)
        itemDict["image"] = images
        # item properties
        itemDict["properties"] = getProperties(detail_html.find("ul", attrs={"class": "attr_list"}))
        # item intro image
        itemDict["introImage"] = getIntroImage(id)
        # item info
        # item_infos = detail_html.find_all("div", attrs={"class": "info_div"})
        # for item_info in item_infos:
        #     key = item_info.find("label").text
        #     value = item_info.find("a", attrs={"class": "selected"})
        #     if value:
        #         value = value.text
        #     else:
        #         value = item_info.find("p").text
        #     itemDict[key] = value
        # add item to set
        setDict[itemA.attrs["href"]] = itemDict
        # break
    file.write(json.dumps(setDict))
    file.close()
