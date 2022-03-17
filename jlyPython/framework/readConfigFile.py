# coding=utf-8
import os

from configparser import ConfigParser


file_path = os.path.dirname(os.path.abspath('.')) + '/testConfig/config.ini'
# file_path = os.path.abspath(os.curdir) + '/testConfig/config.ini'


class ReadConfig:

    # 构造函数，读取配置文件
    def __init__(self):

        self.config = ConfigParser()
        self.config.read(file_path)


    # get some http info from file :config.ini
    def get_http(self, name):
        value = self.config.get("browserType", name)
        return value

    def get_email(self, name):
        value = self.config.get("EMAIL", name)
        return value


    def get_db(self, name):
        value = self.config.get("DATABASE", name)
        return value

