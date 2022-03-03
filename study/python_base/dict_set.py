# -*- coding: utf-8 -*-

# @Time : 2022/2/23 17:35

# @Author : WangJun

# @File : dict_set.py

# @Software: PyCharm

d = {'Michael': 95, 'Bob': 75, 'Tracy': 85}
print(d['Michael'])

# 把数据放入dict的方法，除了初始化时指定外，还可以通过key放入
d['Adam'] = 67

# 通过dict提供的get()方法，如果key不存在，可以返回None，或者自己指定的value：
d.get('Thomas')

# 要删除一个key，用pop(key)方法，对应的value也会从dict中删除：
d.pop('Bob')

# 对于可变对象，比如list，对list进行操作，list内部的内容是会变化的，比如：
a = ['c', 'b', 'a']
print(a.sort())

# 集合
a = [1, 2, 3]
s = set(a)
print(s)

# 通过add(key)方法可以添加元素到set中，可以重复添加，但不会有效果
s.add(4)

# 通过remove(key)方法可以删除元素：
s.remove(4)

# set可以看成数学意义上的无序和无重复元素的集合，因此，两个set可以做数学意义上的交集、并集等操作：
x1 = [1, 2, 3]
x2 = [2, 3, 4]
s1 = set(x1)
s2 = set(x2)
# 交集
print(s1 & s2)

# 并集
print(s1 | s2)
