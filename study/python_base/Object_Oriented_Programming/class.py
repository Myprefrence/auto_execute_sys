# -*- coding: utf-8 -*-

# @Time : 2022/2/24 17:34

# @Author : WangJun

# @File : class.py

# @Software: PyCharm

class Student(object):

    def __init__(self, name, score):
        self.name = name
        self.score = score

    def print_score(self,):
        print('%s: %s' % (self.name, self.score))

    def get_grade(self):
        if self.score >= 90:
            return 'A'
        elif self.score >= 60:
            return 'B'
        else:
            return 'C'


if __name__ == '__main__':
    bart = Student('Bart Simpson', 59)
    bart.print_score()
    print(bart.get_grade())