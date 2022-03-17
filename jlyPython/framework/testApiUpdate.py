#-*-coding:GBK -*-



import unittest
import requests
# from testCase.test_login_A import test_login
import json
import time
import hashlib
import random
token = ""
# 禁用安全请求警告
try:
    requests.packages.urllib3.disable_warnings()
except:
    pass
salt = "*2f4961%8*5B588463bee04djDAed27"
from jlyPython.framework.readExcel import ReadExcel

class testApi(object):
    # def math_sign(self,**kwargs):
    #     api_param = dict(sorted(kwargs.items()))
    #     param_string = ''
    #
    #     for key, value in api_param.items():
    #         param_string = param_string + key + '=' + str(value) + '&'
    #     # print(param_string + "secretValue=" + salt)
    #     return param_string + "secretValue=" + salt
    #
    # def encode_md5(self,str_para):
    #     print(u"加密前的字符串：", str_para)
    #     m = hashlib.md5()
    #     m.update(str_para.encode("utf-8"))
    #     # print(u"加密值为：", m.hexdigest())
    #     return m.hexdigest()

    # def get_time(self):
    #     request_time = int(time.time())
    #     return request_time

    def get_params(self, url, kwargs):
        url = url + '?'
        for key in kwargs:
            url = url + key+'='+kwargs[key]+'&'
        return url[:-1]


    def http_request(self,url,data,method,encryption,):

        headers = {
            "Accept-Encoding": "gzip",
            "Connection": "Keep-Alive",
            "Host": 'demo.cloudv2.voiceaitech.com',

        }
        if encryption:#0:不加密，1:加密
            headers["Content-Type"] = "multipart/form-data"


        else:

            headers["Content-Type"] = "application/json; charset=utf-8"



        # print(headers)
        if method.lower() == 'get':
            url = self.get_params(url, data)
            response = requests.get(url=url, headers=headers,verify=False)
        if method.lower() == 'post' and encryption:
            response = requests.post(url=url, data=data, headers=headers,verify=False)
        if method.lower() == 'post'and not encryption:
            response = requests.post(url=url, data=json.dumps(data), headers=headers,verify=False)

        return response






if __name__ == '__main__':
    # unittest.main(verbosity=2)
    data = ''
    print(type(data))
    url = ''
    t=testApi()
    dict_data = eval(data)
    t.http_request(url=url, method='post', token=token, **dict_data)
