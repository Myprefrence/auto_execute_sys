# -*- coding: utf-8 -*-

# @Time : 2022/2/25 10:24

# @Author : WangJun

# @File : get_object.py

# @Software: PyCharm


# 判断对象类型，使用type()函数
print(type(123))

# 判断class的类型，可以使用isinstance()函数
class Animal(object):
    def run(self):
        print('Animal is running...')

class Dog(object):
    def run(self):
        print('Dog is running...')

a = Animal()
d = Dog()
print(isinstance(a, Animal))

# 使用dir()函数，它返回一个包含字符串的list，比如，获得一个str对象的所有属性和方法
print(dir("ABC"))

class MyObject(object):

    def __init__(self):
        self.x = 9

    def power(self):
        return self.x * self.x

obj = MyObject()

# 配合getattr()、setattr()以及hasattr()，我们可以直接操作一个对象的状态
print('hasattr(obj, \'x\') =', hasattr(obj, 'x')) # 有属性'x'吗？
print('hasattr(obj, \'y\') =', hasattr(obj, 'y')) # 有属性'y'吗？
setattr(obj, 'y', 19) # 设置一个属性'y'

print('hasattr(obj, \'y\') =', hasattr(obj, 'y')) # 有属性'y'吗？
print('getattr(obj, \'y\') =', getattr(obj, 'y')) # 获取属性'y'
print('obj.y =', obj.y) # 获取属性'y'

print('getattr(obj, \'z\') =',getattr(obj, 'z', 404)) # 获取属性'z'，如果不存在，返回默认值404

f = getattr(obj, 'power') # 获取属性'power'
print(f)
print(f())