# -*- coding: utf-8 -*-

# @Time : 2022/3/1 18:15

# @Author : WangJun

# @File : date_encoder.py

# @Software: PyCharm


import datetime
import json


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self, obj)
