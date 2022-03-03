# -*- coding: utf-8 -*-

# @Time : 2022/2/23 16:54

# @Author : WangJun

# @File : for.py

# @Software: PyCharm

n = 1
while n <= 100:
    if n > 10: # 当n = 11时，条件满足，执行break语句
        break # break语句会结束当前循环
    print(n)
    n = n + 1
print('END')

x = 0
while x < 10:
    x = x + 1
    if x % 2 == 0: # 如果n是偶数，执行continue语句
        continue # continue语句会直接继续下一轮循环，后续的print()语句不会执行
    print(x)

sum = 0
for y in range(101):
    sum = sum + y
print(sum)