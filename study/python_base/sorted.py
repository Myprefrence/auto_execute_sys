# -*- coding: utf-8 -*-

# @Time : 2022/2/24 17:25

# @Author : WangJun

# @File : sorted.py

# @Software: PyCharm

# 给sorted传入key函数，即可实现忽略大小写的排序,进行反向排序

a = ['bob', 'about', 'Zoo', 'Credit']
x = sorted(a, key=str.lower, reverse=True)

# 当我们在传入函数时，有些时候，不需要显式地定义函数，直接传入匿名函数更方便
y = list(map(lambda x: x * x,[1, 2, 3, 4, 5, 6, 7, 8, 9]))
print(y)

# 通过对比可以看出，匿名函数lambda x: x * x实际上就是：
def f(x):
    return x * x