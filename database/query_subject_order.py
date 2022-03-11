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
                      f"loan_amt,loan_period,channel,order_status,JSON_EXTRACT(risk_result_json, '$.result_code') as result_code," \
                      f"cap_interest_day,cap_loan_datetime,annual_rate,project_no,rpy_type,id_no," \
                      f"JSON_EXTRACT(ext_json, '$.loanPurpose') as loan_purpose,cust_no,cust_mobile_no,cust_name," \
                      f"acct_name,bank_code,bank_name,acct,bank_phone,loan_period,ext_json from {self.xn}_{self.env}_cbs.t_loan_order " \
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
                sql = f"select project_type,cap_code_json from {self.env}_aps.t_project_info where project_no=%s;"
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
                sql = f"select id_no_platform_id,cust_no from {self.xn}_{self.env}_eam.t_cust_info where id_no=%s;"
                cursor.execute(sql, (id_no, ))
                result = cursor.fetchone()

                return result
        finally:
            self.connection.close()

    def cap(self, loan_id):
        '''提取客户表信息'''

        try:
            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"select cap_code,remark,loan_rate,grace_days,cap_name from {self.xn}_{self.env}_cap.t_loan_apply_info where loan_order_no=%s;"
                cursor.execute(sql, (loan_id, ))
                result = cursor.fetchone()

                return result
        finally:
            self.connection.close()

    def res(self, apply_no):
        '''提取决策信息'''

        try:
            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"select JSON_EXTRACT(req_data, '$.asset_credit_amt') as asset_credit_amount," \
                      f"JSON_EXTRACT(req_data, '$.asset_used_amt') as asset_used_amt from {self.env}_res.t_case_apply_log " \
                      f"where apply_no=%s;"
                cursor.execute(sql, (apply_no, ))
                result = cursor.fetchone()

                return result
        finally:
            self.connection.close()

    def cap_compensatory(self, loan_id):
        '''提取资金代偿信息'''

        try:
            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"select sum(ifnull(repay_total,0)) as 累计代偿金额,sum(ifnull(repay_principal,0)) as 累计代偿本金," \
                      f"sum(ifnull(repay_interest,0)) as 累计代偿利息,sum(ifnull(repay_overdue_interest,0)) as 累计代偿罚息 " \
                      f"from {self.xn}_{self.env}_cap.t_compensatory_info where loan_id = %s;"
                cursor.execute(sql, (loan_id, ))
                result = cursor.fetchone()

                return result
        finally:
            self.connection.close()

    def cbs_rpy_datetime(self, loan_id):
        '''提取订单逾期信息'''

        try:
            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"select max(case when schedule_date>=curdate() then 0 when last_rpy_datetime is null or " \
                      f"substr(last_rpy_datetime,1,10)>=curdate() then datediff(curdate(),schedule_date) when " \
                      f"substr(last_rpy_datetime,1,10)>schedule_date then datediff(last_rpy_datetime,schedule_date) " \
                      f"when substr(last_rpy_datetime,1,10)<=schedule_date then 0 end) as 订单历史最大逾期天数," \
                      f"max(case when schedule_date>=curdate() then 0 when last_rpy_datetime is null or " \
                      f"substr(last_rpy_datetime,1,10)>=curdate() then datediff(curdate(),schedule_date)else 0 end) " \
                      f"as 订单当前逾期天数 from {self.xn}_{self.env}_cbs.t_repay_plan where type='ASSET' and " \
                      f"loan_order_id=%s;"
                cursor.execute(sql, (loan_id, ))
                result = cursor.fetchone()

                return result
        finally:
            self.connection.close()

    def cbs_rpy_principal(self, loan_id):
        '''提取还款信息'''

        try:
            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"select sum(ifnull(rpy_principal,0)) as 已还本金,max(rpy_datetime) as 最近一次还款时间 from " \
                      f"{self.xn}_{self.env}_cbs.t_repay_record where loan_order_id=%s;"
                cursor.execute(sql, (loan_id, ))
                result = cursor.fetchone()

                return result
        finally:
            self.connection.close()

    def cbs_paid_guarantee(self, loan_id):
        '''提取订单担保信息'''

        try:
            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"select sum(ifnull(calculation_process_variable,0)) as 订单已收担保费收入 from " \
                      f"{self.xn}_{self.env}_cbs.t_paid_guarantee_fee_flow_statistics where compute_status = 'success' " \
                      f"and loan_order_id=%s;"
                cursor.execute(sql, (loan_id, ))
                result = cursor.fetchone()

                return result
        finally:
            self.connection.close()

    def cbs_guarantee_fee(self, loan_id):
        '''提取订单担保信息'''

        try:
            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"select sum(ifnull(guarantee_fee,0)) as 订单应收担保费收入 from {self.xn}_{self.env}_cbs.t_guarantee_fee_statistics" \
                      f" where statistics_date = date_format(date_add(curdate(),interval -1 day),'%%Y%%m%%d')" \
                      f" and loan_order_id=%s;"
                cursor.execute(sql, (loan_id, ))
                result = cursor.fetchone()

                return result
        finally:
            self.connection.close()



