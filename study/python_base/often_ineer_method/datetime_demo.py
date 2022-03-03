# -*- coding: utf-8 -*-

# @Time : 2022/2/25 17:20

# @Author : WangJun

# @File : datetime_demo.py

# @Software: PyCharm

from datetime import datetime, timedelta, timezone

# 获取当前时间
now = datetime.now()

# 获取指定日期和时间
dt = datetime(2015, 4, 19, 12, 20)  # 用指定日期时间创建datetime

# datetime转换为timestamp
dt.timestamp() # 把datetime转换为timestamp
# 1429417200.0

# timestamp转换为datetime
t = 1429417200.0
print(datetime.fromtimestamp(t))  # 本地时间
# 2015-04-19 12:20:00

print(datetime.utcfromtimestamp(t))  # UTC时间
# 2015-04-19 04:20:00

# str转换为datetime
cday = datetime.strptime('2015-6-1 18:19:59', '%Y-%m-%d %H:%M:%S')

# datetime转换为str
snow = datetime.now()
print(snow.strftime('%Y-%m-%d %H:%M:%S'))

# datetime加减
rnow = datetime.now()
rnow + timedelta(hours=10)

# 本地时间转换为UTC时间
tz_utc_8 = timezone(timedelta(hours=8))
tnow = datetime.now()
print(tnow)
dt = now.replace(tzinfo=tz_utc_8) # 强制设置为UTC+8:00
print(dt)

# 时区转换
utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
