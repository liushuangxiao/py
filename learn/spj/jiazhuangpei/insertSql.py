# http://dict.baidu.com
# encoding=utf-8
import gzip
import os
import time
import re
import string
import ssl
import json
import base64
import urllib.request
from http import cookiejar
from urllib import parse
from bs4 import BeautifulSoup

product_id = 0

def find_last(string,str):
    last_position=-1
    while True:
        position=string.find(str,last_position+1)
        if position==-1:
            return last_position
        last_position=position


def b64(filename):
    return str(base64.b64encode(filename.encode("utf-8")),'utf-8')


def deb64(filename):
    return base64.b64decode(filename).decode("utf-8")


def getSuffix(filename):
    start = find_last(filename,'.')
    suffix = filename[start:]
    if '?' in suffix:
        suffix = suffix[:suffix.index('?')]
    return suffix


def getFilename(img):
    filename = b64(img) + getSuffix(img)
    filename = filename.replace("/","-s-")
    return filename


def printSql(setNo,name):
    setInfoFile = 'E:/720/jiazhuangpei/%s.txt' % setNo
    sif = open(setInfoFile, 'r', encoding='UTF-8')
    info = json.loads(sif.readline())
    sif.close()

    setInfo = {"image":[ setNo + "/" + getFilename(im) for im in info["image"]], "introImage": [ setNo + "/" + getFilename(im) for im in info["introImage"]]}
    mainItem = info["mainItem"]
    global product_id
    for item in mainItem:
        product_id += 1
        if item not in info:
            print(item + " fail")
            continue
        itemInfo = info[item]
        sqlSetItem ="insert into spj_home.product_set_item(name,product_id,suite,`group`,num,create_time,update_time,choose,product_set_id)" + " values('" + itemInfo["properties"]["分类"] + "'," + str(product_id) + ",1,1,1,'2020-02-27','2020-02-27','" + itemInfo["choose"].replace("沙发分类：","").replace("尺寸：","").replace("颜色：","").replace("颜色分类：","").replace("材质：","").replace("床规格：","").replace("规格：","").replace("类型：","") + "','"+setNo+"');"

        if "：" in sqlSetItem.replace("贵：","").replace("电视柜：","").replace("餐桌：","").replace("餐椅：","").replace("贵妃：","").replace("茶几：","").replace("床头柜：","").replace("把：","").replace("床：",""):
            raise Exception('{}'.format(sqlSetItem))

        priceMap = itemInfo["price"]
        properties = {}
        properties["info"] = itemInfo["properties"]
        properties["image"] = [ setNo + "/" + getFilename(im) for im in itemInfo["image"]]
        properties["introImage"] = [ setNo + "/" + getFilename(im) for im in itemInfo["introImage"]]
        price = {}
        for key in priceMap:
            value = priceMap[key]
            compressPriceMap = {}
            compressPriceMap["name"] = value["sku"]
            compressPriceMap["supply_price"] = value["supply_price"]
            compressPriceMap["feed_price"] = value["feed_price"]
            compressPriceMap["shop_price"] = value["shop_price"]
            compressPriceMap["market_price"] = value["market_price"]
            compressPriceMap["install_price"] = value["install_price"]
            compressPriceMap["price"] = value["price"]
            compressPriceMap["stock"] = value["stock"]
            price[key] = compressPriceMap
        properties["price"] = price
        properties["uri"] = item
        propertiesStr = json.dumps(properties)
        propertiesStr = propertiesStr.encode('utf-8').decode('unicode_escape')
        # propertiesStr = propertiesStr.replace("\\","/").replace("\t","")
        # print(itemInfo)
        item = "insert into spj_home.product(id,name,properties,create_time,update_time,uri) values("+str(product_id)+",'" + itemInfo["name"] + "','" + propertiesStr + "','2020-02-27','2020-02-27','" +item+ "');"
        print(sqlSetItem)
        print(item)

    setInfoStr = json.dumps(setInfo)
    setInfoStr = setInfoStr.encode('utf-8').decode('unicode_escape')
    sql = "insert into spj_home.product_set(id,name,keyword,intro,create_time,update_time,properties) value('"+setNo+"','" + name + "','" + name + "','" + name + "','2020-02-27','2020-02-27','" + setInfoStr + "');"
    print(sql)

# setinfo no
# setNo = '93'
# name = "流云如水"
# setNo = '92'
# name = "秋若水"
# setNo = '83'
# name = "时尚之都"
# setNo = '37'
# name = "暮光森林"
# setNo = '01'
# name = "都市新宠"
# setInfoFile = 'E:/720/jiazhuangpei/%s.txt' % setNo
setMap = [['93',"流云如水"],['92',"秋若水"],['83',"时尚之都"],['37',"暮光森林"],['01',"都市新宠"]]
for s in setMap:
    printSql(s[0], s[1])