# -*- coding: utf-8 -*-

# @Time : 2022/2/28 11:13

# @Author : WangJun

# @File : chardet_demo.py

# @Software: PyCharm

# 使用chardet
# 当我们拿到一个bytes时，就可以对其检测编码。用chardet检测编码，只需要一行代码
import chardet

check = chardet.detect(b'Hello, world!')
print(check)
# {'encoding': 'ascii', 'confidence': 1.0, 'language': ''}
# 检测出的编码是ascii，注意到还有个confidence字段，表示检测的概率是1.0（即100%）

# 检测GBK编码的中文
data = '离离原上草，一岁一枯荣'.encode('gbk')
check_g = chardet.detect(data)
print(check_g)
# {'encoding': 'GB2312', 'confidence': 0.7407407407407407, 'language': 'Chinese'}
# 检测的编码是GB2312，注意到GBK是GB2312的超集，两者是同一种编码，检测正确的概率是74%，language字段指出的语言是'Chinese'

# 对UTF-8编码进行检测
data_u = '离离原上草，一岁一枯荣'.encode('utf-8')
print(chardet.detect(data_u))
# {'encoding': 'utf-8', 'confidence': 0.99, 'language': ''}

# 对日文进行检测
data_r = '最新の主要ニュース'.encode('euc-jp')
print(chardet.detect(data_r))