# -*- coding: utf-8 -*-

# @Time : 2022/1/21 12:37

# @Author : WangJun

# @File : count_twenty_seven.py

# @Software: PyCharm
from database.inner_twenty_seven import *
import datetime
import time

class repay_count:

    def __init__(self, mysql, xn, env, asset_org_no='', bis_type_id=''):
        self.mysql = mysql
        self.env = env
        self.xn = xn
        self.asset_org_no = asset_org_no
        self.bis_type_id = bis_type_id

    def compare_time(self, day1, day2):
        time_array1 = time.strptime(day1, "%Y-%m-%d")
        timestamp_day1 = int(time.mktime(time_array1))
        time_array2 = time.strptime(day2, "%Y-%m-%d")
        timestamp_day2 = int(time.mktime(time_array2))
        result = (timestamp_day2 - timestamp_day1) // 60 // 60 // 24

        return result

    def count_max_overdue_days(self,id_no):
        '''userid_self_prod_max_overdue_days'''
        max_time = []
        project_group = ["1001", "1002"]
        repay_plan = repay(self.mysql, self.xn, self.env, self.asset_org_no, self.bis_type_id).query_action_max_overdue_days_1(id_no)

        for repays in repay_plan:
            repay_settle = repays["repay_settle"]
            project_no = repays["project_no"]
            loan_order_id = repays["loan_order_id"]
            current_period = repays["current_period"]

            if repay_settle == 0:
                if project_no in project_group:
                    repay_plan_1 = repay(self.mysql, self.xn, self.env). \
                        query_action_max_overdue_days_3(current_period, loan_order_id)

                    repay_plan_schedule_total = float(repay_plan_1[0]["schedule_total"])

                    repay_plan_schedule_date = repay_plan_1[0]["schedule_date"]

                    repay_record = repay(self.mysql, self.xn, self.env).\
                        query_action_max_overdue_days_4(current_period, loan_order_id)
                    repay_record_rpy_total_amt = repay_record[0]["sum(rpy_total_amt)"]

                    repay_record_rpy_datetime = repay_record[0]["max(rpy_datetime)"]

                    if repay_record_rpy_datetime is not None:
                        if repay_record_rpy_total_amt >= repay_plan_schedule_total:
                            repay_record_rpy_datetime = str(repay_record_rpy_datetime)[0:10]
                            overdue_time = self.compare_time(repay_plan_schedule_date, repay_record_rpy_datetime)
                            max_time.append(int(overdue_time))

                        elif repay_record_rpy_total_amt < repay_plan_schedule_total:
                            nowtime = str(datetime.datetime.now())[0:10]
                            overdue_time = self.compare_time(repay_plan_schedule_date, nowtime)
                            max_time.append(int(overdue_time))
                    else:
                        nowtime = str(datetime.datetime.now())[0:10]
                        overdue_times = self.compare_time(repay_plan_schedule_date, nowtime)
                        max_time.append(int(overdue_times))

                else:
                    max_repay_time = repay(self.mysql, self.xn, self.env).query_action_max_overdue_days_5(current_period,
                                                                                                          loan_order_id)
                    max_repay_time = max_repay_time[0]['max(DATEDIFF(now(),schedule_date))']
                    max_time.append(int(max_repay_time))

            else:
                repay_plan_2 = repay(self.mysql, self.xn, self.env).query_action_max_overdue_days_2(current_period,
                                                                                                    loan_order_id)
                max_date = repay_plan_2[0]["max(DATEDIFF(last_rpy_datetime,schedule_date))"]
                max_time.append(int(max_date))

        return max(max_time)

    def count_prod_ever_overdue_cnt_tot(self, id_no):
        '''同身份证号,匹配同个产品（资产方+业务类型）下融担机构A有该用户借款申请'''

        loaderID = []
        project_group = ["1001", "1002"]
        repay_plan = repay(self.mysql, self.xn, self.env, self.asset_org_no, self.bis_type_id).query_action_max_overdue_days_1(id_no)

        for repays in repay_plan:
            repay_settle = repays["repay_settle"]
            project_no = repays["project_no"]
            loan_order_id = repays["loan_order_id"]
            current_period = repays["current_period"]

            if repay_settle == 0:
                if project_no in project_group:
                    repay_plan_1 = repay(self.mysql, self.xn, self.env). \
                        query_action_max_overdue_days_3(current_period, loan_order_id)

                    repay_plan_schedule_total = float(repay_plan_1[0]["schedule_total"])

                    repay_plan_schedule_date = repay_plan_1[0]["schedule_date"]

                    repay_record = repay(self.mysql, self.xn, self.env).\
                        query_action_max_overdue_days_4(current_period, loan_order_id)
                    repay_record_rpy_total_amt = repay_record[0]["sum(rpy_total_amt)"]

                    repay_record_rpy_datetime = repay_record[0]["max(rpy_datetime)"]

                    if repay_record_rpy_datetime is not None:
                        if repay_record_rpy_total_amt >= repay_plan_schedule_total:
                            repay_record_rpy_datetime = str(repay_record_rpy_datetime)[0:10]
                            overdue_time = self.compare_time(repay_plan_schedule_date, repay_record_rpy_datetime)
                            if overdue_time > 0:
                                loaderID.append(loan_order_id)

                        elif repay_record_rpy_total_amt < repay_plan_schedule_total:
                            nowtime = str(datetime.datetime.now())[0:10]
                            overdue_time = self.compare_time(repay_plan_schedule_date, nowtime)
                            if overdue_time > 0:
                                loaderID.append(loan_order_id)

                    else:
                        nowtime = str(datetime.datetime.now())[0:10]
                        overdue_times = self.compare_time(repay_plan_schedule_date, nowtime)
                        if overdue_times > 0:
                            loaderID.append(loan_order_id)

                else:
                    loaderId = repay(self.mysql, self.xn, self.env).userid_self_prod_ever_overdue_cnt_tot_2(current_period,
                                                                                                            loan_order_id)
                    if len(loaderId) == 0:
                        continue
                    else:
                        loaderID.append(loaderId[0]["loan_order_id"])

            else:
                loaderId = repay(self.mysql, self.xn, self.env).userid_self_prod_ever_overdue_cnt_tot_1(current_period,
                                                                                                        loan_order_id)
                if len(loaderId) == 0:
                    continue
                else:
                    loaderID.append(loaderId[0]["loan_order_id"])

        return len(set(loaderID))

    def count_prod_overdue_terms_tot(self, id_no):
        '''同身份证号,匹配同个产品（资产方+业务类型）下融担机构A有该用户借款申请，融担机构B有该用户借款申请'''
        bill_no = []

        project_group = ["1001", "1002"]
        repay_plan = repay(self.mysql, self.xn, self.env, self.asset_org_no,
                           self.bis_type_id).query_action_max_overdue_days_1(id_no)

        for repays in repay_plan:
            repay_settle = repays["repay_settle"]
            project_no = repays["project_no"]
            loan_order_id = repays["loan_order_id"]
            current_period = repays["current_period"]

            if repay_settle == 0:
                if project_no in project_group:
                    repay_plan_1 = repay(self.mysql, self.xn, self.env). \
                        userid_self_prod_overdue_terms_tot_1(current_period, loan_order_id)

                    repad_plan_id = repay_plan_1[0]["id"]
                    repay_plan_schedule_total = float(repay_plan_1[0]["schedule_total"])

                    repay_plan_schedule_date = repay_plan_1[0]["schedule_date"]

                    repay_record = repay(self.mysql, self.xn, self.env). \
                        query_action_max_overdue_days_4(current_period, loan_order_id)
                    repay_record_rpy_total_amt = repay_record[0]["sum(rpy_total_amt)"]

                    repay_record_rpy_datetime = repay_record[0]["max(rpy_datetime)"]

                    if repay_record_rpy_datetime is not None:
                        if repay_record_rpy_total_amt >= repay_plan_schedule_total:
                            repay_record_rpy_datetime = str(repay_record_rpy_datetime)[0:10]
                            overdue_time = self.compare_time(repay_plan_schedule_date, repay_record_rpy_datetime)
                            # print("相差值为：%s" %(overdue_time, ))
                            if overdue_time > 0:
                                bill_no.append(repad_plan_id)

                        elif repay_record_rpy_total_amt < repay_plan_schedule_total:
                            nowtime = str(datetime.datetime.now())[0:10]
                            overdue_time = self.compare_time(repay_plan_schedule_date, nowtime)
                            if overdue_time > 0:
                                bill_no.append(repad_plan_id)

                    else:
                        nowtime = str(datetime.datetime.now())[0:10]
                        overdue_times = self.compare_time(repay_plan_schedule_date, nowtime)
                        if overdue_times > 0:
                            bill_no.append(repad_plan_id)

                else:
                    plan_Id = repay(self.mysql, self.xn, self.env).userid_self_prod_overdue_terms_tot_2(
                        current_period, loan_order_id)
                    if len(plan_Id) > 0:
                        bill_no.append(plan_Id[0]["id"])

            else:
                plan_Ids = repay(self.mysql, self.xn, self.env).userid_self_prod_overdue_terms_tot_3(current_period,
                                                                                                     loan_order_id)
                if len(plan_Ids) > 0:
                    bill_no.append(plan_Ids[0]["id"])

        return len(set(bill_no))

if __name__ == '__main__':
    mysql = "adb"
    xn = "dw"
    env = "test1"
    id_no = "CI2201210000800084"
    asset_org_no ="360JR"
    bis_type_id = "0001"
    repay_count_3 = repay_count(mysql, xn, env, asset_org_no, bis_type_id).count_max_overdue_days(id_no)
    repay_count_1 = repay_count(mysql, xn, env, asset_org_no, bis_type_id).count_prod_ever_overdue_cnt_tot(id_no)
    repay_count_2 = repay_count(mysql, xn, env, asset_org_no, bis_type_id).count_prod_overdue_terms_tot(id_no)
    print("count_prod_ever_overdue_cnt_tot的值为：%s" % (repay_count_1, ))
    print("count_prod_overdue_terms_tot的值为：%s" % (repay_count_2,))
    print("count_prod_overdue_terms_tot的值为：%s" % (repay_count_3,))
