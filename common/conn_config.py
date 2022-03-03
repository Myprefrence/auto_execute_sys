# -*- coding: utf-8 -*-

# @Time : 2022/1/11 14:43

# @Author : WangJun

# @File : conn_config.py

# @Software: PyCharm

import configparser
import os


class read_config:

    def __init__(self):
        self.path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.cf = configparser.ConfigParser()
        self.cf.read(self.path + "\config\config.ini")

    def read_project(self, project: str, param):
        result = self.cf.get(project, param)

        return result


if __name__ == '__main__':
    print(read_config().read_project("LeXin", "linux_dir_xna"))
