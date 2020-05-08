# http://dict.baidu.com
# encoding=utf-8
import os
import time
import re
import string
import ssl
import urllib.request
from urllib import parse
from bs4 import BeautifulSoup

path = '/house/19lou/village-%s.txt'
path = 'E:/house/19lou/village-%s.txt'

house_url = 'https://house.19lou.com/newhouse-house-%d&area=%d&name=&price=0&houseType=%d&homeType=%s'

house_types = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
areas_cn = ['上城区', '下城区', '西湖区', '江干区', '拱墅区', '滨江区', '萧山区', '余杭区', '富阳', '临安', '桐庐', '建德', '淳安', '钱塘新区']
areas = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
house_types_cn = ['公寓', '小高层', '高层', '排屋', '别墅', '商铺', '多层', '住宅', '商业', '办公', 'loft公寓', '沿街底商', '洋房', '叠墅', '院墅', '叠排','合院', '联排']
home_types_cn = ['一居室', '二居室', '三居室', '四居室', '五居室', '六居室', '复式室', '跃层']

def getHtml(url):
    max_time = 5
    _time = 0
    print(url, end="")
    while _time < max_time :
        _time += 1
        try:
            page = urllib.request.urlopen(url)
            html = page.read()
            # html = gzip.decompress(html)
            html = html.decode('gb18030').encode('utf-8')
            print(' success')
            return html
        except HTTPError as e:
            print(e)
            time.sleep(20)
            count = 0
            refresh()
    print(' fail')
    return None

def getItems(result):
    items = result.find("ul")
    return items.select("li")

def getD(text):
    da = re.findall(r"\d+", text)
    d = -1
    if (len(da) > 0) :
        d = da[0]
    return str(d)

def getTotal(html):
    _page = html.find("div", attrs={"class": "hs-main-title"})
    _max = 0
    if _page:
        _max = re.findall('\d+',_page.text)[0]
    return _max

def writeUrl(url,file,attribute_reg):
    html = getHtml(url)
    if not html:
        return
    html = BeautifulSoup(html, 'html.parser')
    result = html.find("div", attrs={"class": "ss-result"})
    total = getTotal(result)
    total = int(total)
    if (total == 0):
        return
    max_page = total/10
    items = getItems(result)
    for item in items :
        item_url = item.find("a").attrs['href']
        item_url = "https:" + item_url + "/xq"
        item_html = getHtml(item_url)
        if not item_html:
            return
        item_html = BeautifulSoup(item_html, 'html.parser')
        item_detal = item_html.find("table", attrs={"class": "details"})
        attributes = item_detal.select("tr")
        item_dict = {}
        for attribute in attributes:
            attribute = attribute.select("td")
            item_dict[attribute[0].text.strip()] = attribute_reg.sub('',attribute[1].text)
        price = getD(item_dict.get("价格",''))
        lineA = (item_dict.get("地址",'-'),price,item_dict.get("开发商",'-'),item_dict.get("主力户型",'-'),item_dict.get("开盘时间",'-'),item_dict.get("入住时间",'-'),item_url,str(item_dict).replace(' ',''));
        line = "\t".join(lineA)
        file.write(line)
        file.write("\n")
    file.flush()

ssl._create_default_https_context = ssl._create_unverified_context
opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent',
                      'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
urllib.request.install_opener(opener)

now = time.strftime("%Y%m%d", time.localtime())
filename = path % now
file = open(filename, 'w', encoding='UTF-8')

attribute_reg = re.compile('[\s\?]')

for area in areas:
    for house_type in house_types:
        for home_type in home_types_cn:
            home_type = parse.quote(home_type, safe=string.printable)
            isLastPage = False
            max_page = 1
            page = 1
            while not isLastPage:
                url = house_url % (page, area, house_type, home_type)
                writeUrl(url, file, attribute_reg)
                page += 1
                isLastPage = page > max_page

file.close()