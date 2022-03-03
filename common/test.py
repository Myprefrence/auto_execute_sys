# -*- coding: utf-8 -*-

# @Time : 2022/2/21 15:52

# @Author :Administrator

# @File : HTTP.py

# @Software: PyCharm
# @Desc:http请求：post,get

import requests
import json


class requestsUtils:
    def __init__(self):
        self.s = requests.Session()

    def post_main(self, method, url, data, header):
        global res#可以在函数内部对函数外的对象进行操作了
        if method=="post":
            if header =="application/x-www-form-urlencoded":
                res = self.s.post(url=url, data=data)
                print(res.json())
            if header=={"Content-Type": "application/json"}:
                res = self.s .post(url=url, data=json.dumps(data), headers=header)
                print(res)
        # json.dumps()函数用于将 Python 对象编码成 JSON 字符串
        # return json.dumps(res.json(), ensure_ascii=False, sort_keys=True, indent=4)
        # return res.json()

    def get_main(self,method,url, data, header):
        global res
        if method=="get":
            if header != None:
                res = requests.get(url=url, data=data, headers=header)
            else:
                res = requests.get(url=url, data=data)
        return json.dumps(res.json(), ensure_ascii=False, sort_keys=True, indent=4)#转中文为ensure_ascii=False，



if __name__ == '__main__':
    env = "test2"
    url = 'https://oms' + env + '.jiuliyuntech.com/res-oms/strategyInfo/submitStrategyInfoOnEdit'
    header = {"Content-Type": "application/json"}
    data = {'id': 'A172108260001900074', 'enable': 'Y', 'strategy_code': 'D027', 'strategy_name': 'D027'}
    # header="application/x-www-form-urlencoded"
   # requestsUtils().post_main(method="post",url=url,data=data,header=header)
    res = requests.post(url=url, data=json.dumps(data), headers=header)
    print(res)