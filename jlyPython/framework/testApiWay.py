#-*-coding:GBK -*-



import unittest
import requests
# from testCase.test_login_A import test_login
import json
import time
import hashlib
import random
token = ""

salt = "*2f4961%8*5B588463bee04djDAed27"
from jlyPython.framework.readExcel import ReadExcel

class testApi(object):
    def math_sign(self,**kwargs):
        api_param = dict(sorted(kwargs.items()))
        param_string = ''
        print(api_param)
        for key, value in api_param.items():
            param_string = param_string + key + '=' + str(value) + '&'
        print(param_string + "secretValue=" + salt)
        return param_string + "secretValue=" + salt

    def encode_md5(self,str_para):
        # print(u"加密前的字符串：", str_para)
        m = hashlib.md5()
        m.update(str_para.encode("utf-8"))
        # print(u"加密值为：", m.hexdigest())
        return m.hexdigest()

    def get_time(self):
        request_time = int(time.time())
        return request_time

    def get_params(self, url, **kwargs):
        url = url + '?'
        for key in kwargs:
            url = url + key+'='+kwargs[key]+'&'
        return url[:-1]



    def http_request(self,url, method, token, **kwargs):
        h_nonce = random.randint(1, 10000) + self.get_time()
        headers = {
            "h-time": str(self.get_time() * 1000),
            "h-nonce": str(h_nonce),
            "h-tenant-code": 'gcyh',
            # "h-version": "2.1.4",
            # "h-system-code": "android"
        }
        params = dict(headers, **kwargs)
        headers["h-sign"] = self.encode_md5(self.math_sign(**params))
        headers['h-api-token'] = token
        if method.lower() == 'get':
            url = self.get_params(url, **kwargs)
            response = requests.get(url=url, headers=headers, verify=False).json()
        if method.lower() == 'post':
            response = requests.post(url=url, data=kwargs, headers=headers, verify=False).json()
        return response

# token = "eyJhbGciOiJIUzUxMiJ9.eyJtb2JpbGUiOiIxNTA3NDcwOTEzNCIsInN1YiI6ImI1M2I5MDRjZWZhYTQzMjRiZDE0NjEzMGQ0ZDA0ODJhIiwiaC10ZW5hbnQtY29kZSI6ImdjeWgiLCJsb2dpbklkIjoiMzRmZGQwODUzZjlmNGQxZjlhZDIzNzU0ZjM3MDhhZDQiLCJleHAiOjE1NzEzOTIxMzEsImlhdCI6MTU1NDExMjEzMTc3OH0.CZ5Rqm0QtBlsmVnxJ_yeKkStotHHnjHiQuLPR3JiGH9Yg-khgwAJDryICmmauMAfVBLbVzbEdlwk-AkBDZoDPA"
# url = 'http://test_gateway.guochuangyuanhe.com/api/v1/redpacket/favorite/get'
# data = {"currentPage":"1","pageSize":"10"}
# a= testApi()
# a.http_request(url,"get",token,**data)


# url = 'http://wwdadad.api.com'
# d = {'h-time': '1554198519000', 'h-nonce': '1554204027', 'h-tenant-code': 'gcyh', 'type': 'KSB_type'}
# t = testApi()
# print(t.get_params(url,**d))

if __name__ == '__main__':
    # unittest.main(verbosity=2)
    data = ''
    print(type(data))
    url = ''
    t=testApi()
    dict_data = eval(data)
    t.http_request(url=url, method='post', token=token, **dict_data)

