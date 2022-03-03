# -*- coding: utf-8 -*-

# @Time : 2022/2/25 9:49

# @Author : WangJun

# @File : polymorphic.py

# @Software: PyCharm

"""
同一个事件发生在不同对象上面，就有不同效果，这样的例子叫多态。
输出结果，第一个是10，第二个是15，调用了同样的方法，得到的结果不相同，这就是多态。多态存在的三个必要条件：
1）需要继承

2）需要重写

3）父类引用指向了子类对象
"""

class Animal(object):
    def run(self):
        print('Animal is running...')

class Dog(Animal):
    def run(self):
        print('Dog is running...')

class Cat(Animal):
    def run(self):
        print('Cat is running...')

def run_twice(animal):
    animal.run()
    animal.run()

a = Animal()
d = Dog()
c = Cat()

print('a is Animal?', isinstance(a, Animal))
print('a is Dog?', isinstance(a, Dog))
print('a is Cat?', isinstance(a, Cat))

print('d is Animal?', isinstance(d, Animal))
print('d is Dog?', isinstance(d, Dog))
print('d is Cat?', isinstance(d, Cat))

run_twice(c)

"""
a is Animal? True
a is Dog? False
a is Cat? False
d is Animal? True
d is Dog? True
d is Cat? False
Cat is running...
Cat is running...

"""

