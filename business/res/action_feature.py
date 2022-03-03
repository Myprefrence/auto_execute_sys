from database.query_action import *
from numpy import *
import time
import datetime

class actionFeature:

    def __init__(self, mysql, xn, env, id_no,asset_org_no='', bis_type_id='', project_no=[]):

        self.xn = xn
        self.env = env
        self.id_no = id_no
        self.asset_org_no = asset_org_no
        self.bis_type_id = bis_type_id
        self.project_no = project_no
        self.mysql = mysql
        self.xnv = ["xna", "xnb"]


    def compare_time(self, day1, day2):
        time_array1 = time.strptime(day1, "%Y-%m-%d")
        timestamp_day1 = int(time.mktime(time_array1))
        time_array2 = time.strptime(day2, "%Y-%m-%d")
        timestamp_day2 = int(time.mktime(time_array2))
        result = (timestamp_day2 - timestamp_day1) // 60 // 60 // 24

        return result

    def count_feature_47(self):
        ''' 统计userid_grt_max_overdue_days最大逾期天数 '''
        '''userid_self_prod_max_overdue_days'''
        max_time = []
        project_group = ["1001", "6006", "6013", "1002", "TEST001"]
        repay_plan = Action(self.mysql, self.xn, self.env, self.asset_org_no, self.bis_type_id).query_action_47_1(self.id_no)

        for repays in repay_plan:
            repay_settle = repays["repay_settle"]
            project_no = repays["project_no"]
            loan_order_id = repays["loan_order_id"]
            current_period = repays["current_period"]

            if repay_settle == 0:
                if project_no in project_group:
                    repay_plan_1 = Action(self.mysql, self.xn, self.env). \
                        query_action_47_3(current_period, loan_order_id)

                    repay_plan_schedule_total = float(repay_plan_1[0]["schedule_total"])

                    repay_plan_schedule_date = repay_plan_1[0]["schedule_date"]

                    repay_record = Action(self.mysql, self.xn, self.env). \
                        query_action_47_4(current_period, loan_order_id)
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
                    max_repay_time = Action(self.mysql, self.xn, self.env).query_action_47_5(
                        current_period, loan_order_id)
                    max_repay_time = max_repay_time[0]['max(DATEDIFF(now(),schedule_date))']
                    max_time.append(int(max_repay_time))

            else:
                repay_plan_2 = Action(self.mysql, self.xn, self.env).query_action_47_2(current_period, loan_order_id)
                max_date = repay_plan_2[0]["max(DATEDIFF(last_rpy_datetime,schedule_date))"]
                max_time.append(int(max_date))

        return max(max_time)

    def count_feature_48(self):
        ''' 统计userid_self_prod_cur_overdue_days最大逾期天数 '''
        max_time = []
        project_group = ["1001","6006","6013","1002","TEST001"]
        repay_plan = Action(self.mysql, self.xn, self.env, self.asset_org_no, self.bis_type_id).query_action_48_1(self.id_no)

        for repays in repay_plan:
            repay_settle = repays["repay_settle"]
            project_no = repays["project_no"]
            loan_order_id = repays["loan_order_id"]
            current_period = repays["current_period"]

            if repay_settle == 0:
                if project_no in project_group:
                    repay_plan_1 = Action(self.mysql, self.xn, self.env). \
                        query_action_48_3(current_period, loan_order_id)

                    repay_plan_schedule_total = float(repay_plan_1[0]["schedule_total"])

                    repay_plan_schedule_date = repay_plan_1[0]["schedule_date"]

                    repay_record = Action(self.mysql, self.xn, self.env). \
                        query_action_48_4(current_period, loan_order_id)
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
                    max_repay_time = Action(self.mysql, self.xn, self.env).query_action_48_5(
                        current_period,
                        loan_order_id)
                    max_repay_time = max_repay_time[0]['max(DATEDIFF(now(),schedule_date))']
                    max_time.append(int(max_repay_time))

            else:
                continue

        return max(max_time)

    def count_feature_49(self):
        ''' 统计userid_grt_cur_overdue_days最大当前逾期天数 '''
        max_time = []
        project_group = ["1001", "6006", "6013", "1002", "TEST001"]
        repay_plan = Action(self.mysql, self.xn, self.env, self.asset_org_no, self.bis_type_id).query_action_47_1(self.id_no)
        print(repay_plan)

        for repays in repay_plan:
            repay_settle = repays["repay_settle"]
            project_no = repays["project_no"]
            loan_order_id = repays["loan_order_id"]
            current_period = repays["current_period"]

            if repay_settle == 0:
                if project_no in project_group:
                    repay_plan_1 = Action(self.mysql, self.xn, self.env). \
                        query_action_47_3(current_period, loan_order_id)

                    repay_plan_schedule_total = float(repay_plan_1[0]["schedule_total"])

                    repay_plan_schedule_date = repay_plan_1[0]["schedule_date"]

                    repay_record = Action(self.mysql, self.xn, self.env). \
                        query_action_47_4(current_period, loan_order_id)
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
                    max_repay_time = Action(self.mysql, self.xn, self.env).query_action_47_5(
                        current_period, loan_order_id)
                    max_repay_time = max_repay_time[0]['max(DATEDIFF(now(),schedule_date))']
                    max_time.append(int(max_repay_time))

            else:
                continue

        return max(max_time)




if __name__ == '__main__':
    mysql = "adb"
    xn = "dw"
    env = "test1"
    id_no = "CI2201210000800084"
    asset_org_no ="360JR"
    bis_type_id = "0001"
    project_no = ['ZZX-FENGTAI-LZ', 'zzxyqgdh202101', 'zzxftzb202012', 'zzx-lx-qnyh', 'zzxhx202012',
                  'zzxsnzb202011', 'zzxsnhh202011']

    conn = actionFeature(mysql=mysql, xn=xn, env=env, id_no=id_no, asset_org_no=asset_org_no, bis_type_id=bis_type_id,
                         project_no=project_no)
    # query_count_feature_47 = conn.count_feature_47()
    # query_count_feature_48 = conn.count_feature_48()
    query_count_feature_49 = conn.count_feature_49()

    # print("count_feature_47的值为：%s" % (query_count_feature_47, ))
    # print("count_feature_48的值为：%s" % (query_count_feature_48, ))
    print("count_feature_49的值为：%s" % (query_count_feature_49, ))






