# -*- coding: utf-8 -*-

# @Time : 2022/2/21 11:26

# @Author : WangJun

# @File : query_assert_monitor.py

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

    def cbs_loan_amt(self, project_no, asset_org_no):
        '''计算实担借款本金'''

        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"select sum(loan_amt),id from {self.xn}_{self.env}_cbs.t_loan_order where order_status in" \
                      f"('SETTLED','ON_REPAYMENT') and project_no=%s and asset_org_no=%s;"
                cursor.execute(sql, (project_no, asset_org_no))
                result = cursor.fetchone()

                return result
        finally:
            self.connection.close()

    def cbs_rpy_principal(self, project_no, asset_org_no):
        '''计算实担还款金额'''

        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"select sum(rpy_principal) from {self.xn}_{self.env}_cbs.t_repay_record where project_no=%s " \
                      f"and asset_org_no=%s;"
                cursor.execute(sql, (project_no, asset_org_no ))
                result = cursor.fetchone()

                return result
        finally:
            self.connection.close()

    def cbs_repay_principal(self, project_no):
        '''计算实担代偿金额'''

        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"select sum(repay_principal) from {self.xn}_{self.env}_cap.t_compensatory_info where status='SUCCESS' and " \
                      f"deleted=0 and project_no=%s;"
                cursor.execute(sql, (project_no, ))
                result = cursor.fetchone()

                return result
        finally:
            self.connection.close()

    def pls_loan_principal(self, project_no, asset_org_no):
        '''计算通道借款本金'''

        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"select sum(loan_principal) from {self.xn}_{self.env}_pls.t_order_info where project_no=%s " \
                      f"and asset_org_no=%s;"
                cursor.execute(sql, (project_no, asset_org_no))
                result = cursor.fetchone()

                return result
        finally:
            self.connection.close()

    def pls_repay_record_principal(self, project_no, asset_org_no):
        '''计算通道还款金额'''

        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"select sum(repay_principal) from {self.xn}_{self.env}_pls.t_repay_record where project_no=%s " \
                      f"and asset_org_no=%s;"
                cursor.execute(sql, (project_no, asset_org_no))
                result = cursor.fetchone()

                return result
        finally:
            self.connection.close()

    def pls_compensate_principal(self, project_no, asset_org_no):
        '''计算通道代偿金额'''

        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"select sum(compensate_principal) from {self.xn}_{self.env}_pls.t_compensate_record where " \
                      f"project_no=%s and asset_org_no=%s;"
                cursor.execute(sql, (project_no, asset_org_no))
                result = cursor.fetchone()

                return result
        finally:
            self.connection.close()

    def cbs_compare_quota(self, project_no, warrant_start_time, asset_org_no):
        '''计算实担总放款金额'''

        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"select sum(loan_amt) from {self.xn}_{self.env}_cbs.t_loan_order where order_status " \
                      f"in('SETTLED','ON_REPAYMENT') and project_no=%s and %s <= cap_interest_day <= Now() " \
                      f"and asset_org_no=%s;"
                cursor.execute(sql, (project_no, warrant_start_time, asset_org_no))
                result = cursor.fetchone()

                return result
        finally:
            self.connection.close()

    def pls_compare_quota(self, project_no, warrant_start_time, now_time, asset_org_no):
        '''计算通道总放款金额'''

        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"select sum(loan_principal) from {self.xn}_{self.env}_pls.t_order_info where project_no=%s " \
                      f"and %s <= loan_date <= %s and asset_org_no=%s;"
                cursor.execute(sql, (project_no, warrant_start_time, now_time, asset_org_no))
                result = cursor.fetchone()

                return result
        finally:
            self.connection.close()

    def prs_assert_message(self, assert_no):
        '''统计资产方信息'''

        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"select quota,available_quota,expire_end_datetime,quota_type,monitor_status,monitor_status from " \
                      f"{self.env}_prs.t_asset_quota_info where asset_code=%s and `enable`='Y';"
                cursor.execute(sql, (assert_no,))
                result = cursor.fetchone()

                return result
        finally:
            self.connection.close()
