# -*- coding: utf-8 -*-

# @Time : 2022/2/24 16:54

# @Author : WangJun

# @File : generate.py

# @Software: PyCharm

n = 6
triangle = [[1],[1,1]]
for i in range(2,n):     #已经给出前两行，所以求剩余行
    cur = [1]            #定义每行第一个元素
    pre = triangle[i-1]  #上一行
    for j in range(i-1): #算几次
        cur.append(pre[j] + pre[j+1])
    cur.append(1)
    triangle.append(cur)
print(triangle)

