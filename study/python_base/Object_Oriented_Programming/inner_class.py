# -*- coding: utf-8 -*-

# @Time : 2022/2/24 17:40

# @Author : WangJun

# @File : inner_class.py

# @Software: PyCharm


# 如果要让内部属性不被外部访问，可以把属性的名称前加上两个下划线__，在Python中，
# 实例的变量名如果以__开头，就变成了一个私有变量（private），只有内部可以访问，外部不能访问

class Student(object):
    def __init__(self, name, score):
        self.__name = name
        self.__score = score

    def print_score(self):
        print('%s: %s' % (self.__name, self.__score))

    # 如果外部代码要获取name和score怎么办？可以给Student类增加get_name和get_score这样的方法：
    def get_name(self):
        return self.__name

    def get_score(self):
        return self.__score

    # 如果又要允许外部代码修改score怎么办？可以再给Student类增加set_score方法：
    def set_score(self, score):
        self.__score = score

    def set_name(self, name):
        self.__name = name


if __name__ == '__main__':
    bart = Student('Bart Simpson', 59)
    print(bart.get_name())
    bart.__name = 'New Name'  # 设置__name变量！
    print(bart.__name)