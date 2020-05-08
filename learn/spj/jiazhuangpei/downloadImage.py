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

# setinfo no
setNo = '93'
setNo = '92'
setNo = '83'
setNo = '37'
setNo = '01'
setInfoFile = 'E:/720/jiazhuangpei/%s.txt' % setNo
path = "E:/720/jiazhuangpei/%s/" % setNo


def downloading(url, filename):
    file_path = path + filename
    print(url, end="")
    if os.path.exists(file_path):
        print(' exists')
        return
    try:
        urllib.request.urlretrieve(url, file_path)
        print(' success')
    except Exception as e:
        print(' fail')
        print(e)


def find_last(string,str):
    last_position=-1
    while True:
        position=string.find(str,last_position+1)
        if position==-1:
            return last_position
        last_position=position


def deb64(filename):
    return base64.b64decode(filename).decode("utf-8")


def getFilename(img):
    filename = b64(img) + getSuffix(img)
    filename = filename.replace("/","-s-")
    return filename


def b64(filename):
    return str(base64.b64encode(filename.encode("utf-8")),'utf-8')


def getSuffix(filename):
    start = find_last(filename,'.')
    suffix = filename[start:]
    if '?' in suffix:
        suffix = suffix[:suffix.index('?')]
    return suffix


if os.path.exists(path):
    pass
else:
    os.mkdir(path)


cookie = cookiejar.CookieJar()
cookie_support = urllib.request.HTTPCookieProcessor(cookie)
ssl._create_default_https_context = ssl._create_unverified_context
opener = urllib.request.build_opener(cookie_support)
opener.addheaders = [
    ('User-Agent',
     'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'),
    ('method', 'GET'),
]
urllib.request.install_opener(opener)

now = time.strftime("%Y%m%d", time.localtime())

sif = open(setInfoFile, 'r', encoding='UTF-8')
info = json.loads(sif.readline())
sif.close()

for img in set(info["image"]):
    filename = getFilename(img)
    downloading(img,filename)

img = info["introImage"]
filename = getFilename(img)
downloading(img,filename)

mainItem = info["mainItem"]

for key in mainItem:
    if "/to-dch/goods/" not in key:
        continue
    value = info[key]
    for img in set(value["introImage"]):
        filename = getFilename(img)
        downloading(img,filename)
    for img in set(value["image"]):
        filename = getFilename(img)
        downloading(img,filename)
