#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pymysql

# 打开数据库连接
db = pymysql.connect("116.62.55.27", "hdm434889240", "yu4410460", "hdm434889240_db", charset='utf8' )

# 使用cursor()方法获取操作游标
cursor = db.cursor()

# 使用execute方法执行SQL语句
cursor.execute("SELECT VERSION()")

# 使用 fetchone() 方法获取一条数据
data = cursor.fetchone()

print("Database version : %s " % data)

# 关闭数据库连接
db.close()