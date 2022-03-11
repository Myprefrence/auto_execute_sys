# -*- coding: utf-8 -*-

# @Time : 2022/3/10 16:50

# @Author : WangJun

# @File : query_subject_case_apply.py

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

    def cae_apply(self, apply_no):
        '''提取order信息'''

        try:
            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"select id,apply_no,ifnull(replace(json_extract(req_data,'$.loan_order_id'),'','\"')," \
                      f"concat('ZZX',replace(json_extract(req_data,'$.id'),'','\"'))) as order_id,fb_no,asset_org_no," \
                      f"ifnull(replace(json_extract(req_data,'$.asset_loan_order_no'),'','\"'),replace(json_extract(req_data,'$.fb_order_no'),'','\"')) as asset_loan_order_no," \
                      f"project_no,project_code,project_name,project_version,product_code,biz_no,platform_user_id," \
                      f"platform_mobile_id,id_no,id_type,mobile_no,apply_result,result_code," \
                      f"if(exec_model=2,update_datetime,apply_datetime) as apply_datetime,resp_time,JSON_EXTRACT(req_data, '$.loan_date') as loan_date," \
                      f"JSON_EXTRACT(req_data, '$.loan_term') as loan_term," \
                      f"JSON_EXTRACT(req_data, '$.irr_rate') as irr_rate,JSON_EXTRACT(req_data, '$.loan_amt') as loan_amt," \
                      f"JSON_EXTRACT(req_data, '$.asset_credit_amt') as asset_credit_amt," \
                      f"JSON_EXTRACT(req_data, '$.asset_used_amt') as asset_used_amt,exec_model,req_data,resp_data," \
                      f"enable from {self.env}_res.t_case_apply_log where apply_no=%s " \
                      f"ORDER BY update_datetime desc LIMIT 1;"
                cursor.execute(sql, (apply_no, ))
                result = cursor.fetchone()

                return result
        finally:
            self.connection.close()

    def case_strategy(self, apply_id):
        '''提取案件策略信息'''

        try:
            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"select JSON_EXTRACT(output_data_inner, '$.total_hit_rules') as total_hit_rules," \
                      f"JSON_EXTRACT(output_data, '$.approve_chain') as approve_chain," \
                      f"JSON_EXTRACT(output_data, '$.credit_query_success') as credit_query_success," \
                      f"JSON_EXTRACT(output_data, '$.credit_query_fail') as credit_query_fail," \
                      f"JSON_EXTRACT(output_data, '$.test_general_tag') as test_general_tag," \
                      f"JSON_EXTRACT(output_data, '$.asset_level') as asset_level," \
                      f"JSON_EXTRACT(output_data, '$.tq01_result') as tq01_result," \
                      f"JSON_EXTRACT(output_data, '$.general_random') as general_random," \
                      f"output_data,output_data_inner from {self.env}_res.t_case_strategy_log where " \
                      f"apply_id=%s ORDER BY update_datetime desc LIMIT 1;"
                cursor.execute(sql, (apply_id, ))
                result = cursor.fetchone()

                return result
        finally:
            self.connection.close()
