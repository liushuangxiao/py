# http://dict.baidu.com
# encoding=utf-8
import gzip
import math
import os
import time
import re
import string
import ssl
import urllib.request
from http import cookiejar
from urllib import parse
from bs4 import BeautifulSoup

# 交房年
year = 2019
year_end = 2020
# 交房月
month = 1
month_end = 12

# 嘉兴ssssssss
city_url = 'jx.newhouse.fang.com'
city_prefix = 'jx'
# html encode
city = '%e5%98%89%e5%85%b4'

# 嘉兴
city_url = 'jx.fang.lianjia.com'
city_prefix = 'jx'
# html encode
city = '%e9%87%91%e5%8d%8e'

# 杭州 https://hz.newhouse.fang.com/house/livindate/201912.htm
# city_url = 'hz.fang.lianjia.com'
# city_prefix = 'hz'
# html encode
# city = '%e6%9d%ad%e5%b7%9e'

index = 1
path = '/house/lianjia/%s-%s.txt'
path = 'E:/house/lianjia/%s-%s.txt'
start_house_url = 'https://' + city_url + '/loupan/'
prefix_house_url = 'https://' + city_url + '%s'
page_url = 'https://' + city_url + '/loupan/pg%d/'
debug = False


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
            html = html.decode('utf-8', "ignore")
            # print(html)
            print(' success')
            return html
        except OSError as e:
            page = urllib.request.urlopen(url)
            html = page.read()
            html = gzip.decompress(html)
            html = html.decode('utf-8', "ignore")
            # print(html)
            print(' success error1')
            return html
        else:
            time.sleep(5)
            cookie.clear()
    print(' fail')
    return None


def getItems(result):
    items = result.find_all("div", attrs={"class": "nlc_img"})
    # print(items)
    return items


def getD(text):
    da = re.findall(r"\d+", text)
    d = -1
    if (len(da) > 0):
        d = da[0]
    return str(d)


def getTotal(html):
    items = html.find("div", attrs={"class": "resblock-have-find"})
    i = items.select('span')
    total = i[1].text
    total = int(total)
    # print(total, items)
    return total


def getNextUrl(html, index):
    reg = 'href="(.*)">' + str(index) + '</a>'
    # print(reg, html)
    matchObj = re.search('href="(.*)">' + str(index) + '</a>', html)
    # print(matchObj)
    if matchObj:
        _url = matchObj.group(1)
        _url = prefix_house_url + _url
        if (debug):
            print(_url)
        return _url
    return None


def getNaviDict(naviA):
    naviDict = {}
    for navi in naviA:
        naviDict[navi.text] = 'https:' + navi.attrs['href']
    return naviDict


def setAttr(attrDict, attr_html):
    # print(attr_html)
    attrA = attr_html.select('span')
    if(len(attrA) == 0):
        return
    attr_key = attrA[0].text
    attr_key = attr_key.replace('：', '')
    attrDict[attr_key] = attribute_reg.sub('', attrA[1].text)


def setAttrSpan(attrDict, attr_html):
    attr_value = attr_html.text;
    attr_value = attr_value.strip()
    attr_key = attr_html.find('span').text.strip()
    attr_key = attr_key.replace('：', '')
    attr_value = attr_value.replace(attr_key, "", 1)
    attr_value = attribute_reg.sub('', attr_value)
    attrDict[attr_key] = attr_value


def setAddress(attrDict, item_html):
    matchObj = re.search(r'address=\'(.*)\'', item_html)
    # print(matchObj)
    if matchObj:
        address = matchObj.group(1)
        attrDict['区域'] = address
    matchObj = re.search(r'vcity= \'(.*)\'', item_html)
    # print(matchObj)
    if matchObj:
        address = matchObj.group(1)
        attrDict['市'] = address


def hasNextPage(html, next_page_num):
    result = html.find('a', attrs={'data-page': next_page_num})
    return result


def detail1(detail_html, file, item_dict, item_url):
    matchObj = re.search( r'class="nnlon">详细信息</a>', detail_html)
    if matchObj :
        detail2(detail_html, file, item_dict, item_url)
        return
    detail_html = BeautifulSoup(detail_html, 'html.parser')
    main_left = detail_html.find("div",attrs={"class": "main-left"})
    item_dict['价格'] = getD(main_left.find("div", attrs={"class": "main-info-price"}).text);
    infos = main_left.find_all("ul")
    for info_li in infos[0].find_all('li'):
        setAttr(item_dict, info_li)
    for info_li in infos[1].find_all('li'):
        setAttr(item_dict, info_li)
    for info_li in infos[2].find_all('li'):
        setAttrSpan(item_dict, info_li)
    for info_li in infos[3].find_all('li'):
        setAttr(item_dict, info_li)
    lineA = (item_dict.get("交房月份"),item_dict.get("市",'-'),item_dict.get("区域",'-'),item_dict.get("价格",'-'),item_dict.get("开盘时间",'-'),item_dict.get("交房时间",'-'),item_dict.get('开发 商','-'),item_dict.get("售楼地址",'-'),item_dict.get("楼盘地址",'-'),item_dict.get("主力户型",'-'),item_url,str(item_dict).replace(' ',''));
    line = "\t".join(lineA)
    line = line.replace('[开盘时间详情]', '')
    line = line.replace('开发 商', '开发商')
    # print(line)
    file.write(line)
    file.write("\n")

def detail2(detail_html, file, item_dict, item_url):
    detail_html = BeautifulSoup(detail_html, 'html.parser')
    main_left = detail_html.find("div",attrs={"class": "main-left"})
    item_dict['价格'] = getD(main_left.find("div", attrs={"class": "main-info-price"}).text);
    infos = main_left.find_all("ul")
    for info_li in infos[0].find_all('li'):
        setAttr(item_dict, info_li)
    for info_li in infos[1].find_all('li'):
        setAttr(item_dict, info_li)
    for info_li in infos[2].find_all('li'):
        setAttr(item_dict, info_li)
    for info_li in infos[3].find_all('li'):
        setAttr(item_dict, info_li)
    lineA = (item_dict.get("交房月份"),item_dict.get("市",'-'),item_dict.get("区域",'-'),item_dict.get("价格",'-'),item_dict.get("开盘时间",'-'),item_dict.get("交房时间",'-'),item_dict.get('开发 商','-'),item_dict.get("售楼地址",'-'),item_dict.get("楼盘地址",'-'),item_dict.get("主力户型",'-'),item_url,str(item_dict).replace(' ',''));
    line = "\t".join(lineA)
    line = line.replace('[开盘时间详情]', '')
    line = line.replace('开发 商', '开发商')
    # print(line)
    file.write(line)
    file.write("\n")


def analysisMonth(url, file, date):
    html = getHtml(url)
    if not html:
        return
    html = BeautifulSoup(html, 'html.parser')
    total = getTotal(html)
    if (total == 0):
        return
    result = html.find("div", attrs={"id": "livinlist"})
    analysisItems(result, file, date)

    page = 2
    hasNext = hasNextPage(html.find("li", attrs={"id": "pageList"}), page)
    while hasNext:
        page_url_c = page_url % (city, date, page)
        html = getHtml(page_url_c)
        if not html:
            return
        html = html.replace('\\"', "").replace('\\t', "").replace('\\n', "").replace('\\r', "")
        html = html.replace('\\/\\/', "//")
        html = BeautifulSoup(html, 'html.parser')
        result = html.find("div", attrs={"id": "livinlist"})
        analysisItems(result, file, date)

        page += 1
        hasNext = hasNextPage(html.find("li",attrs={"id": 'pageList'}), page)
    file.flush()

def setCity(attrDict, item_html):
    breadcrumbs = item_html.find("div", attrs={"class": "breadcrumbs"})
    breadcrumbArray = breadcrumbs.find_all("a")
    attrDict['城市'] = breadcrumbArray[2].text.replace('楼盘', '')
    attrDict['区域'] = breadcrumbArray[3].text.replace('楼盘', '')


def analysisItem(url, file):
    item_url = prefix_house_url % url
    html = getHtml(item_url)
    if not html:
        return
    html = BeautifulSoup(html, 'html.parser')
    div_h = html.find("div", attrs={'class': 'box-loupan'})
    p_h = div_h.find_all("p", attrs={'class': 'desc-p'})
    item_dict = {}
    item_dict["价格"] = html.find('p', attrs={'class': 'jiage'}).text.replace('\n','')
    setCity(item_dict, html)
    for p in p_h:
        setAttr(item_dict, p)
    # print(item_dict)
    lineA = (item_dict.get("交房时间"),item_dict.get("城市",'-'),item_dict.get("区域",'-'),item_dict.get("价格",'-'),item_dict.get("最新开盘",'-'),item_dict.get("交房时间",'-'),item_dict.get('开发商','-'),item_dict.get("售楼处地址",'-'),item_dict.get("项目地址",'-'),'-',item_url,str(item_dict).replace(' ',''));
    # print(lineA)
    line = "\t".join(lineA)
    line = line.replace('[开盘时间详情]', '')
    line = line.replace('开发 商', '开发商')
    # print(line)
    file.write(line)
    file.write("\n")

cookie = cookiejar.CookieJar()
cookie_support = urllib.request.HTTPCookieProcessor(cookie)
ssl._create_default_https_context = ssl._create_unverified_context
opener = urllib.request.build_opener(cookie_support)
opener.addheaders = [('User-Agent',
                      'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36')]
urllib.request.install_opener(opener)

now = time.strftime("%Y%m%d", time.localtime())
filename = path % (city_prefix, now)
file = open(filename, 'w', encoding='UTF-8')

attribute_reg = re.compile('[\s\?]')
url = start_house_url
html = getHtml(url)
if not html:
    os._exit()
html = BeautifulSoup(html, 'html.parser')
total = getTotal(html)
if (total == 0):
    os._exit()
result = html.find("ul", attrs={"class": "resblock-list-wrapper"})
result = result.select('li')

for item in result:
    analysisItem(item.find("a").attrs['href'], file )

file.flush()

page = math.ceil(total / 10.0)
page_c = 2
while page_c < page:
    page_c += 1
    url = page_url % page_c
    html = getHtml(url)
    if not html:
        os._exit()
    html = BeautifulSoup(html, 'html.parser')
    total = getTotal(html)
    if (total == 0):
        os._exit()
    result = html.find("ul", attrs={"class": "resblock-list-wrapper"})
    result = result.select('li')

    for item in result:
        analysisItem(item.find("a").attrs['href'], file )
    file.flush()

file.close()
