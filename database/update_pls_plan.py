# -*- coding: utf-8 -*-

# @Time : 2022/3/11 14:42

# @Author : WangJun

# @File : update_pls_plan.py

# @Software: PyCharm
from common.conn_adb import *
from common.conn import *
from common.conn_rds import *

class plan:
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

    def update_pls_plan(self, repay_principal, repay_interest, repay_overdue_interest,last_repay_type,last_repay_date,
                        order_no, nper):
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"UPDATE `{self.xn}_{self.env}_pls`.`t_repay_plan_detail` SET  `repay_principal`=%s,`repay_interest`=%s" \
                      f",`repay_overdue_interest`=%s,`last_repay_type` = %s,`last_repay_date`=%s" \
                      f" where order_no=%s and nper=%s;"

                cursor.execute(sql, (repay_principal, repay_interest, repay_overdue_interest,last_repay_type,last_repay_date,
                                     order_no, nper,))
                # print(sql)

            self.connection.commit()

        finally:
            self.connection.close()

    def updates_pls_plan(self, settled_sign, order_no, nper):
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"UPDATE `{self.xn}_{self.env}_pls`.`t_repay_plan_detail` SET `settled_sign` = %s " \
                      f"where order_no=%s and nper=%s;"

                cursor.execute(sql, (settled_sign, order_no, nper,))
                # print(sql)

            self.connection.commit()

        finally:
            self.connection.close()

    def pls_plan_record(self, order_no, nper):
        try:
            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"select order_no from {self.xn}_{self.env}_pls.t_repay_plan_detail where order_no=%s and nper=%s " \
                      f"and need_repay_principal = repay_principal;"
                cursor.execute(sql, (order_no, nper))
                result = cursor.fetchone()

                return result
        finally:
            self.connection.close()

    def query_pls_plan(self, order_no):
        '''提取订单担保信息'''

        try:
            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"select last_repay_date,nper,need_repay_date from {self.xn}_{self.env}_pls.t_repay_plan_detail" \
                      f" where order_no=%s and settled_sign='N';"
                cursor.execute(sql, (order_no, ))
                result = cursor.fetchall()

                return result
        finally:
            self.connection.close()