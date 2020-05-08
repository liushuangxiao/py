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

# 金华
path = '/house/fang/%s.txt'
path = 'E:/house/fang/%s.txt'
start_house_url = 'https://jh.newhouse.fang.com/house/s/'
prefix_house_url = 'https://jh.newhouse.fang.com'
# 嘉兴
path = '/house/fang/jx%s.txt'
path = 'E:/house/fang/jx%s.txt'
# start_house_url = 'https://jx.newhouse.fang.com/house/s/'
start_house_url = 'https://jx.newhouse.fang.com/house/s/b98/'
prefix_house_url = 'https://jx.newhouse.fang.com'
# 杭州
path = '/house/fang/hz%s.txt'
path = 'E:/house/fang/hz%s.txt'
start_house_url = 'https://hz.newhouse.fang.com/house/s/'
start_house_url = 'https://hz.newhouse.fang.com/house/s/b921/'
prefix_house_url = 'https://hz.newhouse.fang.com'

debug = False
index = 21

def getHtml(url):
    max_time = 5
    _time = 0
    print(url, end="")
    while _time < max_time :
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
        except Exception as e:
            print(' fail \n',e ,'\n', url, end='')
            time.sleep(5)
            cookie.clear()
        else :
            time.sleep(5)
            cookie.clear()
    print(' fail')
    return None

def getItems(result):
    items = result.find_all("div", attrs={"class":"nlc_img"})
    # print(items)
    return items

def getD(text):
    da = re.findall(r"\d+", text)
    d = -1
    if (len(da) > 0) :
        d = da[0]
    return str(d)

def getTotal(html):
    matchObj = re.search( r'href="/house/s/">全部楼盘<span>\((\d*)\)</span></a>', html)
    # print(matchObj)
    if matchObj:
        _total = int(matchObj.group(1))
        if( debug ):
            print(_total)
        return _total
    return 0

def getNextUrl(html, index):
    reg = 'href="(.*)">'+ str(index) + '</a>'
    # print(reg, html)
    matchObj = re.search( 'href="(.*)">'+ str(index) + '</a>', html)
    # print(matchObj)
    if matchObj:
        _url = matchObj.group(1)
        _url = prefix_house_url + _url
        if( debug ):
            print(_url)
        return _url
    return None

def getNaviDict(naviA):
    naviDict = {}
    for navi in naviA :
        naviDict[navi.text] = 'https:' + navi.attrs['href']
    return naviDict

def setAttr(attrDict, attr_html):
    attrA = attr_html.select('div')
    attr_key = attrA[0].text
    attr_key = attr_key.replace('：', '')
    attrDict[attr_key] = attribute_reg.sub('',attrA[1].text)

def setAttrSpan(attrDict, attr_html):
    attr_value = attr_html.text;
    attr_value = attr_value.strip()
    attr_key = attr_html.find('span').text.strip()
    attr_key = attr_key.replace('：', '')
    attr_value = attr_value.replace(attr_key, "", 1)
    attr_value = attribute_reg.sub('',attr_value)
    attrDict[attr_key] = attr_value

def setAddress(attrDict, item_html):
    matchObj = re.search( r'address=\'(.*)\'', item_html)
    # print(matchObj)
    if matchObj:
        address = matchObj.group(1)
        attrDict['区域'] = address
    matchObj = re.search( r'vcity= \'(.*)\'', item_html)
    # print(matchObj)
    if matchObj:
        address = matchObj.group(1)
        attrDict['市'] = address

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
    lineA = (item_dict.get("市",'-'),item_dict.get("区域",'-'),item_dict.get("价格",'-'),item_dict.get("开盘时间",'-'),item_dict.get("交房时间",'-'),item_dict.get('开发 商','-'),item_dict.get("售楼地址",'-'),item_dict.get("楼盘地址",'-'),item_dict.get("主力户型",'-'),item_url,str(item_dict).replace(' ',''));
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
    lineA = (item_dict.get("市",'-'),item_dict.get("区域",'-'),item_dict.get("价格",'-'),item_dict.get("开盘时间",'-'),item_dict.get("交房时间",'-'),item_dict.get('开发 商','-'),item_dict.get("售楼地址",'-'),item_dict.get("楼盘地址",'-'),item_dict.get("主力户型",'-'),item_url,str(item_dict).replace(' ',''));
    line = "\t".join(lineA)
    line = line.replace('[开盘时间详情]', '')
    line = line.replace('开发 商', '开发商')
    # print(line)
    file.write(line)
    file.write("\n")

def writeUrl(url,file,index):
    html = getHtml(url)
    if not html:
        return None
    next_url = getNextUrl(html, index)
    total = getTotal(html)
    if (total == 0):
        return next_url
    html = BeautifulSoup(html, 'html.parser')
    result = html.find("div", attrs={"id": "newhouse_loupai_list"})
    max_page = total/10
    items = getItems(result)
    for item in items :
        item_url = item.find("a").attrs['href']
        item_url = "https:" + item_url
        item_url = 'https://jinrungongyu.fang.com/'
        item_html = getHtml(item_url)
        if not item_html:
            return None
        item_dict = {}
        setAddress(item_dict, item_html)
        matchObj = re.search( r'<a href="(.*)" id="(.*)"  target="_self">楼盘详情</a>', item_html)
        if matchObj :
            detail_html = getHtml('https:' + matchObj.group(1))
            detail1(detail_html, file, item_dict, item_url)
            break
            continue

        matchObj = re.search( r'<a(.*)href="(.*)" id=(.*)target=(.*)>详细信息</a>', item_html)
        if matchObj :
            detail_html = getHtml('https:' + matchObj.group(2))
            detail2(detail_html, file, item_dict, item_url)
            continue

        print(item_url, "   detail  fail")
        # break
    return next_url


cookie = cookiejar.CookieJar()
cookie_support = urllib.request.HTTPCookieProcessor(cookie)
ssl._create_default_https_context = ssl._create_unverified_context
opener = urllib.request.build_opener(cookie_support)
opener.addheaders = [('User-Agent',
                      'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36')]
urllib.request.install_opener(opener)

now = time.strftime("%Y%m%d", time.localtime())
filename = path % now
file = open(filename, 'w', encoding='UTF-8')

attribute_reg = re.compile('[\s\?]')

next_url = start_house_url
while next_url:
    index += 1
    next_url = writeUrl(next_url, file, index)
    # writeUrl(next_url, None)
    # print(next_url)
    file.flush()
    break

file.close()