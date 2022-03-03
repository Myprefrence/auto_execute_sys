# -*- coding: utf-8 -*-

# @Time : 2022/2/25 19:38

# @Author : WangJun

# @File : requests_demo.py

# @Software: PyCharm


# pip install requests

import requests
r = requests.get('https://www.douban.com/') # 豆瓣首页
print(r.status_code)
print(r.text)
print(r.url) # 实际请求的URL
print(r.encoding)
# 无论响应是文本还是二进制内容，我们都可以用content属性获得bytes对象：
print(r.content)

url = "https://www.douban.com/"
# requests默认使用application/x-www-form-urlencoded对POST数据编码。如果要传递JSON数据，可以直接传入json参数：
params = {'key': 'value'}
r = requests.post(url, json=params) # 内部自动序列化为JSON

# 上传文件需要更复杂的编码格式，但是requests把它简化成files参数
upload_files = {'file': open('report.xls', 'rb')}
rf = requests.post(url, files=upload_files)

# 要在请求中传入Cookie，只需准备一个dict传入cookies参数：
cs = {'token': '12345', 'status': 'working'}
rc = requests.get(url, cookies=cs)

# 要指定超时，传入以秒为单位的timeout参数：
rt = requests.get(url, timeout=2.5) # 2.5秒后超时
