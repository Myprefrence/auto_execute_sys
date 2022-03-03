# -*- coding: utf-8 -*-

# @Time : 2022/2/23 16:26

# @Author : WangJun

# @File : list.py

# @Software: PyCharm

classmates = ['Michael', 'Bob', 'Tracy']

# 数据长度
print(len(classmates))
# 第一个元素
print(classmates[0])
# 倒数第二个元素
print(classmates[-2])

# 添加元素
classmates.append('Adam')

# 根据索引位置插入
classmates.insert(1, "Jack")

# 删除末尾的元素
classmates.pop()

# 删除指定位置的元素
classmates.pop(1)

# 把某个元素替换成别的元素，可以直接赋值给对应的索引位置
classmates[1] = "Sarah"