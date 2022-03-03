# -*- coding: utf-8 -*-

# @Time : 2022/2/24 16:41

# @Author : WangJun

# @File : list_generate.py

# @Software: PyCharm

L = []
for x in range(1,11):
    L.append(x*x)

print(L)

c = [x * x for x in range(1, 11)]

# for循环后面还可以加上if判断，这样我们就可以筛选出仅偶数的平方：
e = [x * x for x in range(1, 11) if x % 2 == 0 ]

# 还可以使用两层循环，可以生成全排列
# ['AX', 'AY', 'AZ', 'BX', 'BY', 'BZ', 'CX', 'CY', 'CZ']
d = [m + n for m in 'ABC' for n in 'XYZ']

# 运用列表生成式，可以写出非常简洁的代码。例如，列出当前目录下的所有文件和目录名，可以通过一行代码实现
import os
f = [d for d in os.listdir('.')]  # os.listdir可以列出文件和目录

# for循环其实可以同时使用两个甚至多个变量，比如dict的items()可以同时迭代key和value：
g = {'x': 'A', 'y': 'B', 'z': 'C' }
for k, v in g.items():
    print(k, '=', v)
