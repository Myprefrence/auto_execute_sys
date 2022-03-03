# -*- coding: utf-8 -*-

# @Time : 2022/2/24 16:25

# @Author : WangJun

# @File : function.py

# @Software: PyCharm

def my_abs(x):
    if x >= 0:
        return x
    else:
        return -x

print(my_abs(-99))


def fact(n):
    if n==1:
        return 1
    return n * fact(n - 1)
print(fact(5))