# -*- coding: utf-8 -*-

# @Time : 2022/2/24 17:03

# @Author : WangJun

# @File : iterable.py

# @Software: PyCharm

from collections.abc import Iterable

# 可以使用isinstance()判断一个对象是否是Iterator对象：
print(isinstance((x for x in range(10)), Iterable))