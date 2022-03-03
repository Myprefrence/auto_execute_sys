# -*- coding: utf-8 -*-

# @Time : 2022/2/24 17:07

# @Author : WangJun

# @File : map_reduce.py

# @Software: PyCharm

# map()函数接收两个参数，一个是函数，一个是Iterable，map将传入的函数依次作用到序列的每个元素，并把结果作为新的Iterator返回。
def f(x):
    return x * x

c = [1, 2, 3, 4, 5, 6, 7, 8, 9]
r = map(f, c)
print(list(r))
# [1, 4, 9, 16, 25, 36, 49, 64, 81]

# map()作为高阶函数，事实上它把运算规则抽象了，因此，我们不但可以计算简单的f(x)=x2，还可以计算任意复杂的函数，
# 比如，把这个list所有数字转为字符串：
print(list(map(str, c)))
# ['1', '2', '3', '4', '5', '6', '7', '8', '9']

# reduce把一个函数作用在一个序列[x1, x2, x3, ...]上，这个函数必须接收两个参数，
# reduce把结果继续和序列的下一个元素做累积计算，其效果就是：
from functools import reduce
def add(x, y):
    return x + y

y = reduce(add, c)
print(y)