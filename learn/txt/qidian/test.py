# coding=utf-8
import re
import urllib.request
import ssl
import gzip


def getHtml(url):
    page = urllib.request.urlopen(url)
    html = page.read()
    # html = gzip.decompress(html)
    html = html.decode('gb18030')
    return html


def getImg(html):
    reg = r'<p class="img_title">(.*)</p>'
    img_title = re.compile(reg)
    imglist = re.findall(img_title, html)
    return imglist

ssl._create_default_https_context = ssl._create_unverified_context
opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent',
                      'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
urllib.request.install_opener(opener)
urls = ['https://house.19lou.com/newhouse-house-1&area=1&name=&price=0&houseType=1&homeType=%E4%B8%80%E5%B1%85%E5%AE%A4','https://house.19lou.com/newhouse-house-1&area=1&name=&price=0&houseType=1&homeType=%E4%BA%8C%E5%B1%85%E5%AE%A4','https://house.19lou.com/newhouse-house-1&area=1&name=&price=0&houseType=1&homeType=%E4%B8%89%E5%B1%85%E5%AE%A4','https://house.19lou.com/newhouse-house-1&area=1&name=&price=0&houseType=1&homeType=%E5%9B%9B%E5%B1%85%E5%AE%A4','https://house.19lou.com/newhouse-house-1&area=1&name=&price=0&houseType=1&homeType=%E4%BA%94%E5%B1%85%E5%AE%A4','https://house.19lou.com/newhouse-house-1&area=1&name=&price=0&houseType=1&homeType=%E5%85%AD%E5%B1%85%E5%AE%A4','https://house.19lou.com/newhouse-house-1&area=1&name=&price=0&houseType=1&homeType=%E5%A4%8D%E5%BC%8F%E5%AE%A4','https://house.19lou.com/newhouse-house-1&area=1&name=&price=0&houseType=1&homeType=%E8%B7%83%E5%B1%82','https://house.19lou.com/newhouse-house-1&area=1&name=&price=0&houseType=2&homeType=%E4%B8%80%E5%B1%85%E5%AE%A4','https://house.19lou.com/newhouse-house-1&area=1&name=&price=0&houseType=2&homeType=%E4%BA%8C%E5%B1%85%E5%AE%A4','https://house.19lou.com/newhouse-house-1&area=1&name=&price=0&houseType=2&homeType=%E4%B8%89%E5%B1%85%E5%AE%A4','https://house.19lou.com/newhouse-house-1&area=1&name=&price=0&houseType=2&homeType=%E5%9B%9B%E5%B1%85%E5%AE%A4'
]
for url in urls:
    url = "https://house.19lou.com/newhouse-house-1&area=0&name=&price=0&houseType=0&homeType=0"
    html = getHtml(url)
    print(html)
