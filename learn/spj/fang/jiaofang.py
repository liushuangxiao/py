# http://dict.baidu.com
# encoding=utf-8
import gzip
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

# 嘉兴
city_url = 'jx.newhouse.fang.com'
city_prefix = 'jx'
# html encode
city = '%e5%98%89%e5%85%b4'

# 嘉兴
city_url = 'jh.newhouse.fang.com'
city_prefix = 'jh'
# html encode
city = '%e9%87%91%e5%8d%8e'

# 杭州 https://hz.newhouse.fang.com/house/livindate/201912.htm
# city_url = 'hz.newhouse.fang.com'
# city_prefix = 'hz'
# html encode
# city = '%e6%9d%ad%e5%b7%9e'

index = 1
path = '/house/fang/jiaofang/%s-%s.txt'
path = 'E:/house/fang/jiaofang/%s-%s.txt'
start_house_url = 'https://' + city_url + '/house/livindate/%s.htm'
prefix_house_url = 'https://%s' % city_url
page_url = 'https://' + city_url + '/house/ajaxrequest/livindateListGet.php?city=%s&month=%s&page=%d'
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
            html = gzip.decompress(html)
            html = html.decode('gb18030', "ignore")
            # print(html)
            print(' success')
            return html
        except OSError as e:
            page = urllib.request.urlopen(url)
            html = page.read()
            html = html.decode('gb18030', "ignore")
            # print(html)
            print(' success')
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
    items = html.find("div", attrs={"class": "nrtr"})
    i = items.select('i')
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
    attrA = attr_html.select('div')
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

def analysisItems(result, file, date):
    items = getItems(result)
    index = 0
    for item in items :
        index += 1
        item_url = item.find("a").attrs['href']
        if(item_url == '//'):
            print("# %s %d fail" % (date, index))
            continue
        item_url = "https:" + item_url
        item_html = getHtml(item_url)
        if not item_html:
            return None
        item_dict = {}
        setAddress(item_dict, item_html)
        item_dict['交房月份'] = date
        matchObj = re.search( r'<a href="(.*)" id="(.*)"  target="_self">楼盘详情</a>', item_html)
        if matchObj :
            detail_html = getHtml('https:' + matchObj.group(1))
            detail1(detail_html, file, item_dict, item_url)
            continue

        matchObj = re.search( r'<a(.*)href="(.*)" id=(.*)target=(.*)>详细信息</a>', item_html)
        if matchObj :
            detail_html = getHtml('https:' + matchObj.group(2))
            detail2(detail_html, file, item_dict, item_url)
            continue

        print(item_url, "   detail  fail")
        # break
    return next_url


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

next_url = ''
while year <= year_end and month <= month_end:
    date = "%04d%02d" % (year, month)
    next_url = start_house_url % date
    analysisMonth(next_url, file, date)
    file.flush()
    if (month == 12):
        month = 1
        year += 1
    else:
        month += 1

file.close()
