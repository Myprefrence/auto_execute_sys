"""
通用的处理数据的方法
"""

import configparser
import datetime
import os
import time


# 获取指定时间差(单位: 秒)的时间
# return_str: 返回结果数据类型 True-str False-datetime
def get_datetime(datetime_target: str or datetime.datetime, seconds_diff=0, return_str=False):
    if not isinstance(datetime_target, datetime.datetime):
        datetime_target = datetime.datetime.strptime(datetime_target, '%Y-%m-%d %H:%M:%S')

    datetime_result = datetime_target + datetime.timedelta(seconds=seconds_diff)
    return datetime_result if not return_str else datetime_result.__format__('%Y-%m-%d %H:%M:%S')


# 获取指定时间格式字符的时间戳
def get_timestamp(datetime_target: str or datetime.datetime, size=13):
    if not isinstance(datetime_target, str):
        datetime_target = datetime_target.__format__('%Y-%m-%d %H:%M:%S')
    return int(time.mktime(time.strptime(datetime_target, '%Y-%m-%d %H:%M:%S'))) * (10 ** (size - 10))


# 获取项目根目录
def get_root_path():
    path = os.getcwd().split('\\')
    return rf'{path[0]}\{path[1]}'

def configs_path():
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return path

# 获取配置文件内容
def get_config(file_path: str):
    config_path = os.path.join(configs_path(), file_path)

    config = configparser.ConfigParser()
    config.read(config_path, encoding='utf-8')
    return config

