# -*- coding: utf-8 -*-

# @Time : 2022/2/25 14:23

# @Author : WangJun

# @File : property.py

# @Software: PyCharm

"""
Python内置的@property装饰器就是负责把一个方法变成属性调用的
@property的实现比较复杂，我们先考察如何使用。把一个getter方法变成属性，只需要加上@property就可以了，
此时，@property本身又创建了另一个装饰器@score.setter，负责把一个setter方法变成属性赋值，
于是，我们就拥有一个可控的属性操作
"""
class Student(object):

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self,value):
        if not isinstance(value, int):
            raise ValueError('score must be an integer!')
        if value < 0 or value > 100:
            raise ValueError('score must between 0 ~ 100!')
        self._score = value


if __name__=='__main__':
    s = Student()
    s.score = 60
    print(s.score)