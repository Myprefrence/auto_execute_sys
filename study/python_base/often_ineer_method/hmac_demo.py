# -*- coding: utf-8 -*-

# @Time : 2022/2/25 18:50

# @Author : WangJun

# @File : hmac_demo.py

# @Software: PyCharm


# Python自带的hmac模块实现了标准的Hmac算法。我们来看看如何使用hmac实现带key的哈希。
#
# 我们首先需要准备待计算的原始消息message，随机key，哈希算法，这里采用MD5，使用hmac的代码如下
import hmac

message = b"Hello, world!"
key = b'secret'
h = hmac.new(key, message, digestmod='MD5')
print(h.hexdigest())
