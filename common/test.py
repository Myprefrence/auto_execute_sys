# -*- coding: utf-8 -*-

# @Time : 2022/2/21 15:52

# @Author :Administrator

# @File : HTTP.py

# @Software: PyCharm
# @Desc:http请求：post,get
import datetime

import requests
import json
import time

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return time.mktime(obj.timetuple())
        else:
            return json.JSONEncoder.default(self, obj)


##首字母转大写:传入list返回list
def listToList(list):
    info = {}
    list_result = []
    for dic in list:#遍历list

        for k,v in dic.items():
            if k.find("_") >= 0:
                str = k.split("_")
                # print(str)
                str1=str[0]
                str2=str[1].capitalize()
                str=str1+str2
                info[str]=v

            else:
                info[k] = v
        list_result.append(dict(info))

    return list_result

if __name__ == '__main__':
    dic=[{'id': 'A062203040006340582', 'object_id': 'A172203040005100015', 'object_code': 'D027',
      'object_version': '20210825-010', 'object_type': 'strategy_outbound', 'var_code': 'credit_query',
      'var_name': '待查询三方', 'data_type': '1', 'category': '2', 'required': 'N', 'spec_type': None, 'use_type': '1',
      'optional': 'Y', 'default_value': '', 'remark': '', 'create_datetime': datetime.datetime(2022, 3, 4, 15, 6, 11),
      'update_datetime': datetime.datetime(2022, 3, 4, 15, 6, 11), 'create_by': 'LIANGHUIHUI',
      'update_by': 'LIANGHUIHUI', 'enable': 'Y'},
     {'id': 'A062203040006340583', 'object_id': 'A172203040005100015', 'object_code': 'D027',
      'object_version': '20210825-010', 'object_type': 'strategy_outbound', 'var_code': 'next_credit_step',
      'var_name': '下一征信步骤', 'data_type': '1', 'category': '2', 'required': 'N', 'spec_type': None, 'use_type': '1',
      'optional': 'Y', 'default_value': '', 'remark': None, 'create_datetime': datetime.datetime(2022, 3, 4, 15, 6, 11),
      'update_datetime': datetime.datetime(2022, 3, 4, 15, 6, 11), 'create_by': 'LIANGHUIHUI',
      'update_by': 'LIANGHUIHUI', 'enable': 'Y'}]

    print(json.dumps(listToList(dic), cls=DateEncoder, ensure_ascii=False))
