# -*- coding: utf-8 -*-

# @Time : 2022/3/2 17:07

# @Author : WangJun

# @File : HTTPS.py

# @Software: PyCharm

# -*- coding: utf-8 -*-

# @Time : 2022/2/21 17:52
# @Author :Administrator
# @File : Https.py
# @Software: PyCharm
# @Desc:http请求：业务系统用到的请求
import requests

import json


class jly_http:
    def __init__(self):
        self.s = requests.Session()
    #九里云平台登录
    def jly_login(self,env):
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "uname": "risk",
            "pwd": "risk@2021&&"
        }
        url = "https://oms{}.jiuliyuntech.com/sso-oms/loginByAjax".format(env)
        response = self.s.post(url=url, data=data, headers=headers).json()
        return response
    #修改中的策略提交
    def jly_commit(self, env, data):
        self.jly_login(env)
        url='https://oms{}.jiuliyuntech.com/res-oms/strategyInfo/submitStrategyInfoOnEdit'.format(env)
        header={"Content-Type": "application/json", "isTest": "true"}
        response =self.s.post(url=url, data=json.dumps(data), headers=header)
        print(response)

if __name__ == '__main__':
    # jly_http().jly_login("test2")
    data = {'id': 'A172108260001900074', 'enable': 'Y', 'strategyCode': 'D027', 'strategyName': 'D027'}
    jly_http().jly_commit("test2", data)
