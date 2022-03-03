# -*- coding: utf-8 -*-

# @Time : 2022/2/25 18:53

# @Author : WangJun

# @File : itertools_demo.py

# @Software: PyCharm

# Python的内建模块itertools提供了非常有用的用于操作迭代对象的函数。

import itertools

# count()会创建一个无限的迭代器，所以上述代码会打印出自然数序列，根本停不下来，只能按Ctrl+C退出
natuals = itertools.count(1)
for n in natuals:
    print(n)

# cycle()会把传入的一个序列无限重复下去
cs = itertools.cycle('ABC')
for c in cs:
    print(c)

# repeat()负责把一个元素无限重复下去，不过如果提供第二个参数就可以限定重复次数
ns =itertools.repeat("A", 3)
for n in ns:
    print(n)

# 无限序列虽然可以无限迭代下去，但是通常我们会通过takewhile()等函数根据条件判断来截取出一个有限的序列：
ns = itertools.takewhile(lambda x: x <= 10, natuals)
print(list(ns))
# [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# chain()可以把一组迭代对象串联起来，形成一个更大的迭代器：
for c in itertools.chain('ABC', 'XYZ'):
    print(c)
# 迭代效果：'A' 'B' 'C' 'X' 'Y' 'Z'

# groupby()把迭代器中相邻的重复元素挑出来放在一起：
for key, group in itertools.groupby('AAABBBCCAAA'):
    print(key, list(group))

# A ['A', 'A', 'A']
# B ['B', 'B', 'B']
# C ['C', 'C']
# A ['A', 'A', 'A']