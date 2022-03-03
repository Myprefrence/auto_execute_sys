# -*- coding: utf-8 -*-

# @Time : 2022/2/24 16:36

# @Author : WangJun

# @File : iteration.py

# @Software: PyCharm

d = {'a': 1, 'b': 2, 'c': 3}
for key in d:
    print(key)

x= ['A', 'B', 'C']
for i, value in enumerate(x):
    print(i, value)

for x, y in [(1, 1), (2, 4), (3, 9)]:
    print(x, y)