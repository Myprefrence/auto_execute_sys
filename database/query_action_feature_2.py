# -*- coding: utf-8 -*-

# @Time : 2022/2/9 9:57

# @Author : WangJun

# @File : query_action_feature_2.py

# @Software: PyCharm


from common.conn_adb import *
from common.conn import *

class repay:

    def __init__(self, mysql, xn, env, asset_org_no='', bis_type_id=''):
        # Connect to the database
        if mysql == "adb":
            self.connection = connect_adb().conn_mysql()
        elif mysql == "jly":
            self.connection = connects().conn_mysql()
        self.env = env
        self.xn = xn
        self.asset_org_no = asset_org_no
        self.bis_type_id = bis_type_id


    def userid_grt_max_loan_withdraw_amt_3m(self, id_no):
        '''放款时间在距今3个月内的订单，计算max(放款金额)'''

        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"SELECT id,loan_amt,cap_interest_day FROM {self.xn}_{self.env}_cbs.t_loan_order WHERE cust_no in (select cust_no from" \
                      f" {self.xn}_{self.env}_eam.t_cust_info where id_no_platform_id=%s) AND project_no IN " \
                      f"( SELECT project_no FROM {self.env}_nls.t_project_line WHERE project_line = 'guarantee' and status='1')" \
                      f" AND order_status IN ('ON_REPAYMENT', 'SETTLED');"
                cursor.execute(sql, (id_no, ))
                result = cursor.fetchall()

                return result
        finally:
            self.connection.close()

    def userid_grt_max_loan_withdraw_amt_6m(self, id_no):
        '''放款时间在距今6个月内的订单，计算max(放款金额)'''

        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"SELECT id,loan_amt,cap_interest_day FROM {self.xn}_{self.env}_cbs.t_loan_order WHERE cust_no in (select cust_no from" \
                      f" {self.xn}_{self.env}_eam.t_cust_info where id_no_platform_id=%s) AND project_no IN " \
                      f"( SELECT project_no FROM {self.env}_nls.t_project_line WHERE project_line = 'guarantee' and status='1')" \
                      f" AND order_status IN ('ON_REPAYMENT', 'SETTLED');"
                cursor.execute(sql, (id_no, ))
                result = cursor.fetchall()

                return result
        finally:
            self.connection.close()

    def userid_grt_max_loan_withdraw_amt_12m(self, id_no):
        '''放款时间在距今12个月内的订单，计算max(放款金额)'''

        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"SELECT id,loan_amt,cap_interest_day FROM {self.xn}_{self.env}_cbs.t_loan_order WHERE cust_no in (select cust_no from" \
                      f" {self.xn}_{self.env}_eam.t_cust_info where id_no_platform_id=%s) AND project_no IN " \
                      f"( SELECT project_no FROM {self.env}_nls.t_project_line WHERE project_line = 'guarantee' and status='1')" \
                      f" AND order_status IN ('ON_REPAYMENT', 'SETTLED');"
                cursor.execute(sql, (id_no, ))
                result = cursor.fetchall()

                return result
        finally:
            self.connection.close()

    def userid_all_max_loan_withdraw_amt_6m_1(self, id_no):
        '''匹配所有项目（不区分通道/实担）放款时间在距今6个月内的订单，计算max(放款金额)'''
        '''通道'''

        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"SELECT id,loan_principal,loan_date FROM {self.xn}_{self.env}_pls.t_order_info WHERE cust_no in " \
                      f"(select cust_no from {self.xn}_{self.env}_eam.t_cust_info where id_no_platform_id=%s);"
                cursor.execute(sql, (id_no, ))
                result = cursor.fetchall()

                return result
        finally:
            self.connection.close()

    def userid_all_max_loan_withdraw_amt_6m_2(self, id_no):
        '''匹配所有项目（不区分通道/实担）放款时间在距今6个月内的订单，计算max(放款金额)'''
        '''实担'''

        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"SELECT id,loan_amt,cap_interest_day FROM {self.xn}_{self.env}_cbs.t_loan_order WHERE cust_no in (select cust_no from" \
                      f" {self.xn}_{self.env}_eam.t_cust_info where id_no_platform_id=%s) AND order_status IN ('ON_REPAYMENT', 'SETTLED');"
                cursor.execute(sql, (id_no, ))
                result = cursor.fetchall()

                return result
        finally:
            self.connection.close()

    def userid_all_max_loan_withdraw_amt_12m_1(self, id_no):
        '''匹配所有项目（不区分通道/实担）放款时间在距今12个月内的订单，计算max(放款金额)'''

        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"SELECT id,loan_principal,loan_date FROM {self.xn}_{self.env}_pls.t_order_info WHERE cust_no in " \
                      f"(select cust_no from {self.xn}_{self.env}_eam.t_cust_info where id_no_platform_id=%s);"
                cursor.execute(sql, (id_no, ))
                result = cursor.fetchall()

                return result
        finally:
            self.connection.close()

    def userid_grt_min_loan_withdraw_amt_tot(self,id_no):
        '''项目的所有资金放款成功的借款申请，计算min(放款金额)'''

        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"SELECT min(loan_amt) FROM {self.xn}_{self.env}_cbs.t_loan_order WHERE cust_no in (select cust_no from" \
                      f" {self.xn}_{self.env}_eam.t_cust_info where id_no_platform_id=%s) AND project_no IN " \
                      f"( SELECT project_no FROM {self.env}_nls.t_project_line WHERE project_line = 'guarantee' and status='1')" \
                      f" AND order_status IN ('ON_REPAYMENT', 'SETTLED');"
                cursor.execute(sql, (id_no, ))
                result = cursor.fetchall()

                return result
        finally:
            self.connection.close()

    def userid_all_min_loan_withdraw_amt_tot_1(self, id_no):
        '''匹配所有项目（不区分通道/实担）放款时间的订单，计算min(放款金额)'''
        '''通道'''

        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"SELECT min(loan_principal) FROM {self.xn}_{self.env}_pls.t_order_info WHERE cust_no in " \
                      f"(select cust_no from {self.xn}_{self.env}_eam.t_cust_info where id_no_platform_id=%s);"
                cursor.execute(sql, (id_no, ))
                result = cursor.fetchall()

                return result
        finally:
            self.connection.close()

    def userid_all_min_loan_withdraw_amt_tot_2(self, id_no):
        '''匹配所有项目（不区分通道/实担）放款时间的订单，计算min(放款金额)'''
        '''实担'''

        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"SELECT min(loan_amt) FROM {self.xn}_{self.env}_cbs.t_loan_order WHERE cust_no in (select cust_no from" \
                      f" {self.xn}_{self.env}_eam.t_cust_info where id_no_platform_id=%s) AND order_status IN ('ON_REPAYMENT', 'SETTLED');"
                cursor.execute(sql, (id_no, ))
                result = cursor.fetchall()

                return result
        finally:
            self.connection.close()

    def userid_psg_loan_withdraw_orgcnt_1m(self, id_no):
        '''匹配项目条线表中所有project_no对应的project_line=‘passage’的项目的放款时间在距今1个月内的订单，计算count(distinct资产方编号)'''

        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"SELECT id,loan_date,asset_org_no FROM {self.xn}_{self.env}_pls.t_order_info WHERE cust_no in " \
                      f"(select cust_no from {self.xn}_{self.env}_eam.t_cust_info where id_no_platform_id=%s) " \
                      f"AND project_no IN ( SELECT project_no FROM {self.env}_nls.t_project_line WHERE " \
                      f"project_line = 'passage' and status='1');"
                cursor.execute(sql, (id_no, ))
                result = cursor.fetchall()

                return result
        finally:
            self.connection.close()

    def userid_self_prod_15d_settle_terms_tot_1(self, id_no):
        '''筛选其中已结清并且结清日期 - 放款日期 +1天<=15天 的订单，匹配这些订单对应的账单，计算count(distinct账单编号)'''

        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"select id,cap_interest_day,loan_period from {self.xn}_{self.env}_cbs.t_loan_order where cust_no in (select" \
                      f" cust_no from {self.xn}_{self.env}_eam.t_cust_info where id_no_platform_id=%s)" \
                      f" and order_status='SETTLED' and bis_type_id='{self.bis_type_id}' and asset_org_no='{self.asset_org_no}';"
                cursor.execute(sql, (id_no, ))
                result = cursor.fetchall()

                return result
        finally:
            self.connection.close()

    def userid_self_prod_15d_settle_terms_tot_2(self, current_period, loan_order_id):
        '''筛选其中已结清并且结清日期 - 放款日期 +1天<=15天 的订单，匹配这些订单对应的账单，计算count(distinct账单编号)'''

        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"SELECT id, last_rpy_datetime from {self.xn}_{self.env}_cbs.t_repay_plan where type ='CBS' and repay_settle=1" \
                      f" and current_period=%s and loan_order_id=%s;"
                cursor.execute(sql, (current_period, loan_order_id))
                result = cursor.fetchall()

                return result
        finally:
            self.connection.close()

    def userid_self_prod_15d_settle_terms_tot_3(self, loan_order_id):
        '''筛选其中已结清并且结清日期 - 放款日期 +1天<=15天 的订单，匹配这些订单对应的账单，计算count(distinct账单编号)'''

        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"SELECT id from {self.xn}_{self.env}_cbs.t_repay_plan where type ='CBS' and repay_settle=1" \
                      f" and loan_order_id=%s;"
                cursor.execute(sql, (loan_order_id, ))
                result = cursor.fetchall()

                return result
        finally:
            self.connection.close()

    def userid_userid_self_prod_last_loan_withdraw_date(self, id_no):
        '''所有资金放款成功的借款申请，计算max(放款时间）'''

        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"SELECT max(cap_interest_day) FROM {self.xn}_{self.env}_cbs.t_loan_order where bis_type_id='{self.bis_type_id}' and " \
                      f"asset_org_no='{self.asset_org_no}' and cust_no in (select cust_no from {self.xn}_{self.env}_eam.t_cust_info where " \
                      f"id_no_platform_id=%s) and order_status in('ON_REPAYMENT','SETTLED');"
                cursor.execute(sql, (id_no, ))
                result = cursor.fetchall()

                return result
        finally:
            self.connection.close()