# -*- coding: utf-8 -*-

# @Time : 2022/3/1 15:24

# @Author : WangJun

# @File : query_subject_user.py

# @Software: PyCharm

from common.conn_adb import *
from common.conn import *
from common.conn_rds import *

class repay:

    def __init__(self, mysql, xn, env):
        # Connect to the database
        if mysql == "adb":
            self.connection = connect_adb().conn_mysql()
        elif mysql == "jly":
            self.connection = connects().conn_mysql()
        elif mysql == "rds":
            self.connection = connect_rds().conn_mysql()
        else:
            print("无此环境！！")
        self.env = env
        self.xn = xn

    def eam_message(self, id_no):
        '''提取用户信息'''

        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"select c.cust_no,c.id_no_platform_id,a.mobile_no_platform_id,c.id_no,a.mobile_no,c.id_no,c.cust_name," \
                      f"a.cust_nation,a.id_address,a.id_issue_date,a.id_expire_date from {self.xn}_{self.env}_eam.t_cust_info as c INNER JOIN " \
                      f"{self.xn}_{self.env}_eam.t_asset_cust_info as a on c.cust_no=a.cust_no where c.id_no=%s ORDER BY " \
                      f"a.create_datetime desc LIMIT 1;"
                cursor.execute(sql, (id_no, ))
                result = cursor.fetchone()

                return result
        finally:
            self.connection.close()

    def cbs_idNo_message(self,id_no):
        '''提取訂單信息'''

        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"select create_datetime,replace(JSON_EXTRACT(ext_json, '$.idCert'), '\"','') " \
                      f"from {self.xn}_{self.env}_cbs.t_loan_order where cust_no in (select cust_no from {self.xn}_{self.env}_eam.t_cust_info " \
                      f"where id_no = %s) ORDER BY create_datetime ASC LIMIT 1;"
                cursor.execute(sql, (id_no, ))
                result = cursor.fetchone()

                return result
        finally:
            self.connection.close()

    def cust_info_message(self,id_no):
        '''提取用户實名信息'''

        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"select acct,bank_code,bank_name,bank_phone from {self.xn}_{self.env}_cbs.t_loan_order where cust_no in " \
                      f"(select cust_no from {self.xn}_{self.env}_eam.t_cust_info where id_no = %s)  ORDER BY " \
                      f"create_datetime DESC LIMIT 1;"
                cursor.execute(sql, (id_no, ))
                result = cursor.fetchone()

                return result
        finally:
            self.connection.close()

