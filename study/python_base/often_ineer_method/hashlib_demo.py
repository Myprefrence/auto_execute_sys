# -*- coding: utf-8 -*-

# @Time : 2022/2/25 17:50

# @Author : WangJun

# @File : hashlib_demo.py

# @Software: PyCharm


# Python的hashlib提供了常见的摘要算法，如MD5，SHA1等等。
#
# 什么是摘要算法呢？摘要算法又称哈希算法、散列算法。它通过一个函数，
# 把任意长度的数据转换为一个长度固定的数据串（通常用16进制的字符串表示）。
import hashlib
md5 = hashlib.md5()
md5.update('how to use md5 in python hashlib?'.encode('utf-8'))
print(md5.hexdigest())

# 如果数据量很大，可以分块多次调用update()，最后计算的结果是一样的：
md5.update('how to use md5 in '.encode('utf-8'))
md5.update('python hashlib?'.encode('utf-8'))
print(md5.hexdigest())