# encoding=utf-8
import time
import json
import sys

# 添加绝对路径。
# 当然，你这样 os.path.abspath(os.path.curdir) 也可以
sys.path.extend(["E:\py\py2\py\learn\spj\dataInsert"])

from szm import szm

file = open("桂花城家具清单11.22", 'r', encoding="UTF-8")

styles = {"现代": 9, "现代中式": 10, "欧式": 11, "美式": 12, "日式": 13, "轻奢": 14}

id = 83
setId = 2
suit = None
# 桂花城 8 幢 801
pre = "ghc/8/801/"
setName = "现代中式"
setStyle = styles["现代中式"]
data = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
totalPrice = 0

productSqls = []
setItemSqls = []
itemUrls = []
urlPre = "http://owner.91spj.com/"

for line in file:
    col = line.strip().split("\t")
    if suit != col[-1]:
        suit = col[-1]

    totalPrice += float(col[9])

    properties = {"uri": "",
                  "info": {"分类": "单椅", "型号": "", "材质": "实木榉木框架+布艺", "规格": "700*680*730mm", "颜色": "图片色", "风格": "现代中式",
                           "商品名称": "三人沙发"}, "image": [], "price": {
            "实木榉木框架+布艺：700*680*730mm": {"name": "实木榉木框架+布艺：700*680*730mm", "price": "8000", "stock": "1308",
                                        "feed_price": "7500", "shop_price": "7800", "market_price": "7900",
                                        "supply_price": "4500", "install_price": "0.00"}}, "introImage": []}
    image = pre + "{0}/{1}.jpg".format(szm.getPinyin(col[-1]), szm.getPinyin(col[3]))
    properties["image"].append(image)

    properties["info"]["分类"] = col[3]
    properties["info"]["材质"] = col[5]
    properties["info"]["规格"] = col[4]
    properties["info"]["颜色"] = col[2] or "图片色"
    properties["info"]["商品名称"] = col[3]

    key = properties["info"]["材质"] + "_" + properties["info"]["规格"]
    properties["price"][key] = {'name': key, 'price': col[9], 'stock': 1000, 'feed_price': col[9], "shop_price": col[9],
                                "market_price": col[9], "supply_price": col[7], "install_price": "0.00"}

    properties["introImage"].append(image)

    # product sql
    sql = "INSERT INTO `spj_home`.`product`(`id`, `name`, `properties`, `status`, `access`, `sales`, `create_time`, `update_time`, `on_sale`, `hot`, `newer`, `discount`, `stock`, `uri`, `max_price`, `min_price`) VALUES ({0}, '{3}', '{1}', 1, 0, 0, '" + data + "','" + data + "', b'1', b'0', b'0', b'0', 1000, null, {9}, {9});"

    col[1] = json.dumps(properties, ensure_ascii=False)
    col[0] = id
    productSqls.append(sql.format(*col))

    # set item sql
    sql = "INSERT INTO `spj_home`.`product_set_item`(`name`, `price`, `product_id`, `suite`, `group`, `num`, `def`,`create_time`,`update_time`,`choose`,`product_set_id`, `cover`)VALUES ( '{3}', {9}, {0}, '" + \
          col[-1] + "', 0, {6}, b'1','" + data + "','" + data + "', '" + key + "'," \
          + str(setId) + ",'" + image + "');"
    setItemSqls.append(sql.format(*col))

    url = urlPre + "product/item?id=" + str(id)
    itemUrls.append("%s\t%s\t%s" % (col[-1], col[3],url))

    id += 1


for s in productSqls:
    print(s)

for s in setItemSqls:
    print(s)

# set sql
sql = "INSERT INTO `spj_home`.`product_set`(`id`, `name`, `style`, `max_price`, `min_price`, `keyword`, `intro`, `status`, `access`, `sales`, `create_time`, `update_time`, `properties`) VALUES(" + str(
    setId) + ",'" + setName + "','" + str(setStyle) + "'," + str(totalPrice) + "," + str(totalPrice) + \
      ",'" + setName + "','" + setName + "',1,0,0,'" + data + "','" + data + "', '{\"vrs\": [{\"qr\": \"\", \"vr\": \"\"}], \"image\": [], \"introImage\": []}');"
print(sql)

print("-------- url ---------------------")

for s in itemUrls:
    print(s)
print("整套方案\t" + urlPre + "product/set/item?id=" + str(setId))
file.close()
