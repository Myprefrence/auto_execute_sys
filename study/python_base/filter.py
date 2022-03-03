# -*- coding: utf-8 -*-

# @Time : 2022/2/24 17:20

# @Author : WangJun

# @File : filter.py

# @Software: PyCharm


# filter()也接收一个函数和一个序列。和map()不同的是，filter()把传入的函数依次作用于每个元素，
# 然后根据返回值是True还是False决定保留还是丢弃该元素。

x = [1, 2, 4, 5, 6, 9, 10, 15]
def is_odd(n):
    return n % 2 == 1

y = list(filter(is_odd, x))
print(y)
# [1, 5, 9, 15]

def not_empty(s):
    return s and s.strip()

list(filter(not_empty, ['A', '', 'B', None, 'C', '  ']))
# 结果: ['A', 'B', 'C']