# -*- coding: utf-8 -*-

# @Time : 2022/1/21 12:51

# @Author : WangJun

# @File : conn_adb.py

# @Software: PyCharm


import configparser
import os
import pymysql



# root_dir = os.path.dirname(os.path.abspath('.'))
# configPath = root_dir + "\config\config.ini"
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(configPath)

cf = configparser.ConfigParser()
cf.read(path + "\config\config.ini")  # 拼接得到config.ini文件的路径，直接使用

secs = cf.sections()  # 获取文件中所有的section(一个配置文件中可以有多个配置，如数据库相关的配置，邮箱相关的配置，每个section由[]包裹，即[section])，并以列表的形式返回

# options = cf.options("Mysql")  # 获取某个section名为Mysql-Database所对应的键
# print(options)
# items = cf.items("Mysql")  # 获取section名为Mysql-Database所对应的全部键值对
# print(items)


class connect_adb:

    def __init__(self):
        self.host = cf.get("ADB", "host")
        self.user = cf.get("ADB", "user")
        self.password = cf.get("ADB", "password")
        self.db = cf.get("ADB", "db")
        self.port = cf.get("ADB", "port")
        self.charset = cf.get("ADB", "charset")

    def conn_mysql(self):
        connection = pymysql.connect(host=self.host,
                                     user=self.user,
                                     password=self.password,
                                     db=self.db,
                                     port=int(self.port),
                                     charset=self.charset,
                                     cursorclass=pymysql.cursors.DictCursor)

        return connection
