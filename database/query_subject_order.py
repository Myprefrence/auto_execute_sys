# -*- coding: utf-8 -*-

# @Time : 2022/3/8 10:39

# @Author : WangJun

# @File : query_subject_order.py

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

    def order(self, asset_loan_order_no):
        '''提取order信息'''

        try:
            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"select id,cap_loan_order_no,asset_loan_no,asset_loan_order_no,asset_org_no,asset_org_name," \
                      f"project_no,project_name,bis_type_id,bis_type_name,loan_apply_datetime," \
                      f"JSON_EXTRACT(ext_json, '$.creditAmt') as creditAmt,JSON_EXTRACT(ext_json, '$.usedAmt') as usedAmt," \
                      f"loan_amt,loan_period,channel,order_status,JSON_EXTRACT(risk_result_json, '$.result_code')," \
                      f"cap_interest_day,cap_loan_datetime,annual_rate,project_no,rpy_type,id_no," \
                      f"JSON_EXTRACT(ext_json, '$.loanPurpose') as loan_purpose,cust_no,cust_mobile_no,cust_name," \
                      f"acct_name,bank_code,bank_name,acct,bank_phone,ext_json from {self.xn}_{self.env}_cbs.t_loan_order " \
                      f"where asset_loan_order_no= %s and order_status in ('SETTLED','ON_REPAYMENT');"
                cursor.execute(sql, (asset_loan_order_no, ))
                result = cursor.fetchone()

                return result
        finally:
            self.connection.close()

    def aps(self, project_no):
        '''提取项目信息'''

        try:
            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"select project_type from {self.env}_aps.t_project_info where project_no=%s;"
                cursor.execute(sql, (project_no, ))
                result = cursor.fetchone()

                return result
        finally:
            self.connection.close()

    def eam_assert_cust(self, cust_no):
        '''提取资产客户表信息'''

        try:
            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"select asset_cust_no,mobile_no_platform_id from {self.xn}_{self.env}_eam.t_asset_cust_info where " \
                      f"cust_no=%s;"
                cursor.execute(sql, (cust_no, ))
                result = cursor.fetchone()

                return result
        finally:
            self.connection.close()

    def eam_cust_info(self, id_no):
        '''提取客户表信息'''

        try:
            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"select id_no_platform_id from {self.xn}_{self.env}_eam.t_cust_info where id_no=%s;"
                cursor.execute(sql, (id_no, ))
                result = cursor.fetchone()

                return result
        finally:
            self.connection.close()

