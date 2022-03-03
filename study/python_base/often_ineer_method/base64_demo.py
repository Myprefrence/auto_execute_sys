# -*- coding: utf-8 -*-

# @Time : 2022/2/25 17:46

# @Author : WangJun

# @File : base64_demo.py

# @Software: PyCharm

import base64

# Python内置的base64可以直接进行base64的编解码：
base64.b64encode(b'binary\x00string')