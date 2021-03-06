# -*- coding: utf-8 -*-

# @Time : 2022/3/1 17:52

# @Author : WangJun

# @File : parse_idNo.py

# @Software: PyCharm
import datetime


class GetInformation(object):

    def __init__(self, id):
        self.id = id
        self.birth_year = int(self.id[6:10])
        self.birth_month = int(self.id[10:12])
        self.birth_day = int(self.id[12:14])

    def get_birthday(self):
        """通过身份证号获取出生日期"""
        birthday = "{0}-{1}-{2}".format(self.birth_year, self.birth_month, self.birth_day)
        birthday_datetime = datetime.datetime.strptime(birthday, '%Y-%m-%d')
        birthday_str = datetime.datetime.strftime(birthday_datetime, '%Y-%m-%d')
        return birthday_str

    def get_sex(self):
        """男生：1 女生：2"""
        num = int(self.id[16:17])
        if num % 2 == 0:
            return 2
        else:
            return 1

    def get_age(self):
        """通过身份证号获取年龄"""
        now = (datetime.datetime.now() + datetime.timedelta(days=1))
        year = now.year
        month = now.month
        day = now.day

        if year == self.birth_year:
            return 0
        else:
            if self.birth_month > month or (self.birth_month == month and self.birth_day > day):
                return year - self.birth_year - 1
            else:
                return year - self.birth_year


id = '110110199509255713'
birthday = GetInformation(id).get_birthday()  # 1995-09-25
age = GetInformation(id).get_age()  # 23
