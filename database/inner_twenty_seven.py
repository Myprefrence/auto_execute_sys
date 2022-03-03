# -*- coding: utf-8 -*-

# @Time : 2022/1/21 11:08

# @Author : WangJun

# @File : inner_twenty_seven.py

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

    def query_action_max_overdue_days_1(self, id_no):
        '''根据用户id查询repay_settle, loan_order_id,current_period,project_no'''
        '''userid_self_prod_max_overdue_days'''
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"select repay_settle, loan_order_id,current_period,project_no from {self.xn}_{self.env}_cbs.t_repay_plan " \
                      f"where loan_order_id in (SELECT id from {self.xn}_{self.env}_cbs.t_loan_order where order_status " \
                      f"in ('ON_REPAYMENT','SETTLED') and `type`= 'CBS' and bis_type_id=%s and asset_org_no=%s and cust_no " \
                      f"in (select cust_no from {self.xn}_{self.env}_eam.t_cust_info where id_no_platform_id=%s));"
                cursor.execute(sql, (self.bis_type_id, self.asset_org_no, id_no, ))
                result = cursor.fetchall()
                # result = result[0]['max(datediff( NOW(), schedule_date ))']
                return result
        finally:
            self.connection.close()

    def query_action_max_overdue_days_2(self, current_period, loan_order_id):
        '''如果repay_title=1时，查询还款计划表最大逾期天数'''
        '''userid_self_prod_max_overdue_days'''
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"SELECT max(DATEDIFF(last_rpy_datetime,schedule_date)) from {self.xn}_{self.env}_cbs.t_repay_plan where " \
                      f"current_period=%s and loan_order_id=%s;"
                cursor.execute(sql, (current_period, loan_order_id, ))
                result = cursor.fetchall()

                return result
        finally:
            self.connection.close()

    def query_action_max_overdue_days_3(self, current_period:int, loan_order_id:str):
        '''如果repay_title=0时，查询还款计划表的schedule_total,schedule_date'''
        '''userid_self_prod_max_overdue_days'''
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"select schedule_total,schedule_date from {self.xn}_{self.env}_cbs.t_repay_plan where current_period=%s and " \
                      f"loan_order_id=%s;"
                cursor.execute(sql, (current_period, loan_order_id, ))
                result = cursor.fetchall()
                return result
        finally:
            self.connection.close()

    def query_action_max_overdue_days_4(self, current_period:int, loan_order_id:str):
        '''如果repay_title=0时，查询还款记录中总已还款金额，最大还款时间'''
        '''userid_self_prod_max_overdue_days'''
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"select sum(rpy_total_amt),max(rpy_datetime) from {self.xn}_{self.env}_cbs.t_repay_record where rpy_period=%s and " \
                      f"loan_order_id=%s;"
                cursor.execute(sql, (current_period, loan_order_id, ))
                result = cursor.fetchall()

                return result
        finally:
            self.connection.close()

    def query_action_max_overdue_days_5(self, current_period, loan_order_id):
        '''如果实还金额小于应还金额时，当前时间减应还时间'''
        '''userid_self_prod_max_overdue_days'''
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"SELECT max(DATEDIFF(now(),schedule_date)) from {self.xn}_{self.env}_cbs.t_repay_plan where current_period=%s and " \
                      f"loan_order_id=%s;"
                cursor.execute(sql, (current_period, loan_order_id, ))
                result = cursor.fetchall()

                return result
        finally:
            self.connection.close()

    def query_action_max_overdue_days_6(self, rpy_datetime, current_period, loan_order_id):
        '''如果实还金额大于等于于应还金额时，实还时间减应还时间'''
        '''userid_self_prod_max_overdue_days'''
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"SELECT max(DATEDIFF(%s,schedule_date)) from {self.xn}_{self.env}_cbs.t_repay_plan where current_period=%s and " \
                      f"loan_order_id=%s;"
                cursor.execute(sql, (rpy_datetime, current_period, loan_order_id ))
                result = cursor.fetchall()

                return result
        finally:
            self.connection.close()


    def userid_self_prod_ever_overdue_cnt_tot_1(self, current_period:int, loan_order_id:str):
        '''当repay_title=1时，取实还时间减应还时间大于0的订单'''

        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"SELECT loan_order_id from {self.xn}_{self.env}_cbs.t_repay_plan where current_period=%s and " \
                      f"loan_order_id=%s and DATEDIFF(last_rpy_datetime,schedule_date)>0;"
                cursor.execute(sql, (current_period, loan_order_id))
                result = cursor.fetchall()

                return result
        finally:
            self.connection.close()

    def userid_self_prod_ever_overdue_cnt_tot_2(self, current_period, loan_order_id):
        '''如果实还金额小于应还金额时，当前时间减应还时间 > 0的订单号'''
        '''userid_self_prod_ever_overdue_cnt_tot'''
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"SELECT loan_order_id from {self.xn}_{self.env}_cbs.t_repay_plan where current_period=%s and " \
                      f"loan_order_id=%s and DATEDIFF(now(),schedule_date)>0;"
                cursor.execute(sql, (current_period, loan_order_id, ))
                result = cursor.fetchall()
                return result
        finally:
            self.connection.close()

    def userid_self_prod_overdue_terms_tot_1(self, current_period, loan_order_id):
        '''如果repay_title=0时，查询还款计划表的schedule_total,schedule_date,id'''
        '''userid_self_prod_overdue_terms_tot'''
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"select id,schedule_total,schedule_date from {self.xn}_{self.env}_cbs.t_repay_plan where current_period=%s and " \
                      f"loan_order_id=%s;"
                cursor.execute(sql, (current_period, loan_order_id, ))
                result = cursor.fetchall()
                return result
        finally:
            self.connection.close()

    def userid_self_prod_overdue_terms_tot_2(self, current_period, loan_order_id):
        '''如果实还金额小于应还金额时，当前时间减应还时间 > 0的订单编号'''
        '''userid_self_prod_overdue_terms_tot'''
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"SELECT id from {self.xn}_{self.env}_cbs.t_repay_plan where current_period=%s and " \
                      f"loan_order_id=%s and DATEDIFF(now(),schedule_date)>0;"
                cursor.execute(sql, (current_period, loan_order_id, ))
                result = cursor.fetchall()
                return result
        finally:
            self.connection.close()

    def userid_self_prod_overdue_terms_tot_3(self, current_period, loan_order_id):
        '''当repay_title=1时，取实还时间减应还时间大于0的订单'''

        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"SELECT id from {self.xn}_{self.env}_cbs.t_repay_plan where current_period=%s and " \
                      f"loan_order_id=%s and DATEDIFF(last_rpy_datetime,schedule_date)>0;"
                cursor.execute(sql, (current_period, loan_order_id))
                result = cursor.fetchall()

                return result
        finally:
            self.connection.close()


if __name__ == '__main__':
    load_id = "XNAC092201211933110004020091"
    mysql = "adb"
    xn = "dw"
    env = "test1"
    id_no = "CI2201210000800084"
    asset_org_no ="360JR"
    bis_type_id = "0001"
    r = repay(mysql, xn, env,asset_org_no, bis_type_id).userid_self_prod_ever_overdue_cnt_tot_2(2, load_id)
    s = len(r)
    print(s)
    if len(r) != 0:
        print(True)
    else:
        print(False)
    print(r)
