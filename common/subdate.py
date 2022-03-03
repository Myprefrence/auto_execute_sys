# -*- coding: utf-8 -*-

# @Time : 2022/1/20 11:50

# @Author : WangJun

# @File : subdate.py

# @Software: PyCharm


#-*- encoding:UTF-8 -*-
from datetime import date
import time
nowtime = date.today()
def convertstringtodate(stringtime):
  "把字符串类型转换为date类型"
  if stringtime[0:2] == "20":
    year=stringtime[0:4]
    month=stringtime[4:6]
    day=stringtime[6:8]
    begintime=date(int(year),int(month),int(day))
    return begintime
  else :
    year="20"+stringtime[0:2]
    month=stringtime[2:4]
    day=stringtime[4:6]
    begintime=date(int(year),int(month),int(day))
    return begintime

def comparetime(nowtime,stringtime):
  "比较两个时间,并返回两个日期之间相差的天数"
  if isinstance(nowtime,date):
    pass
  else:
    nowtime=convertstringtodate(nowtime)
  if isinstance(stringtime,date):
    pass
  else:
    stringtime=convertstringtodate(stringtime)
  result=nowtime-stringtime
  return result.days


# print(isinstance("20141012",date))
# # print(comparetime(nowtime,"140619"))
#
# print(comparetime(nowtime, "211118"))
#
import datetime

d1 = datetime.date(2022, 1, 21)
d2 = datetime.date(2020, 4, 10)
print((d1 - d2).days)







def demo(day1, day2):
  time_array1 = time.strptime(day1, "%Y-%m-%d")
  timestamp_day1 = int(time.mktime(time_array1))
  time_array2 = time.strptime(day2, "%Y-%m-%d")
  timestamp_day2 = int(time.mktime(time_array2))
  result = (timestamp_day2 - timestamp_day1) // 60 // 60 // 24
  return result

date1 = "2021-04-18"
date2 = "2021-04-26 15:34:03"
date3 = date2[0:10]


print(demo(date1,date3))

