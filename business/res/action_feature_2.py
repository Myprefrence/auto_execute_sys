# -*- coding: utf-8 -*-

# @Time : 2022/2/9 9:53

# @Author : WangJun

# @File : action_feature_2.py

# @Software: PyCharm



from database.query_action_feature_2 import *
import datetime
import time
from dateutil.parser import parse

class repay_count:

    def __init__(self, mysql, xn, env, asset_org_no='', bis_type_id=''):
        self.mysql = mysql
        self.env = env
        self.xn = xn
        self.asset_org_no = asset_org_no
        self.bis_type_id = bis_type_id

    def months(self, str1, str2):
        year1 = datetime.datetime.strptime(str1[0:10], "%Y-%m-%d").year
        year2 = datetime.datetime.strptime(str2[0:10], "%Y-%m-%d").year
        month1 = datetime.datetime.strptime(str1[0:10], "%Y-%m-%d").month
        month2 = datetime.datetime.strptime(str2[0:10], "%Y-%m-%d").month
        num = (year1 - year2) * 12 + (month1 - month2)

        return num

    def compare_time(self, day1, day2):
        # 把一个格式化时间字符串转化为struct_time
        time_array1 = time.strptime(day1, "%Y-%m-%d")
        # 将一个struct_time转化为时间戳
        timestamp_day1 = int(time.mktime(time_array1))
        time_array2 = time.strptime(day2, "%Y-%m-%d")
        timestamp_day2 = int(time.mktime(time_array2))
        result = (timestamp_day2 - timestamp_day1) // 60 // 60 // 24

        return result

    def get_early_date(self, target_date: datetime.datetime, month_diff: int):
        target_year = target_date.year
        target_month = target_date.month - month_diff
        if target_month <= 0:
            target_year -= 1
            target_month = 12 - abs(target_month)
        target_day = target_date.day
        target_hour = target_date.hour
        target_minute = target_date.minute
        target_second = target_date.second
        if target_year % 4 != 0 and target_month == 2 and target_day > 28:
            target_day = 28
        if target_year % 4 == 0 and target_month == 2 and target_day > 29:
            target_day = 29
        if target_month in (4, 6, 9, 11) and target_day > 30:
            target_day = 30
        return datetime.datetime.strptime(
            f'{target_year}-{target_month}-{target_day} {target_hour}:{target_minute}:{target_second}',
            '%Y-%m-%d %H:%M:%S')

    def count_userid_grt_max_loan_withdraw_amt_3m(self, id_no):
        '''计算107内部特征变量'''
        loanAmt = []
        value = repay(self.mysql, self.xn, self.env).userid_grt_max_loan_withdraw_amt_3m(id_no)
        for count_value in value:
            loan_id = count_value['id']

            loan_amt = count_value['loan_amt']

            loan_apply_datetime = count_value['cap_interest_day']

            date = datetime.datetime.now()
            # now_time = date.strftime('%Y-%m-%d %H:%M:%S')
            count_month = self.get_early_date(date, 3)

            if loan_apply_datetime >= count_month and loan_apply_datetime <= date:
                loanAmt.append(loan_amt)
            else:
                continue
        print(loanAmt)
        if len(loanAmt) == 0:
            return 0
        else:
            return max(loanAmt)

    def count_userid_grt_max_loan_withdraw_amt_6m(self, id_no):
        '''计算108内部特征变量'''
        loanAmt = []
        value = repay(self.mysql, self.xn, self.env).userid_grt_max_loan_withdraw_amt_6m(id_no)
        for count_value in value:
            loan_id = count_value['id']
            loan_amt = count_value['loan_amt']
            loan_apply_datetime = count_value['cap_interest_day']
            date = datetime.datetime.now()
            # now_time = date.strftime('%Y-%m-%d %H:%M:%S')
            count_month = self.get_early_date(date, 6)

            if loan_apply_datetime >= count_month and loan_apply_datetime <= date:
                loanAmt.append(loan_amt)
            else:
                continue

        if len(loanAmt) == 0:
            return 0
        else:
            return max(loanAmt)

    def count_userid_grt_max_loan_withdraw_amt_12m(self, id_no):
        '''计算109内部特征变量'''
        loanAmt = []
        value = repay(self.mysql, self.xn, self.env).userid_grt_max_loan_withdraw_amt_12m(id_no)
        for count_value in value:
            loan_id = count_value['id']
            loan_amt = count_value['loan_amt']
            loan_apply_datetime = count_value['cap_interest_day']
            date = datetime.datetime.now()
            # now_time = date.strftime('%Y-%m-%d %H:%M:%S')
            count_month = self.get_early_date(date, 12)

            if loan_apply_datetime >= count_month and loan_apply_datetime <= date:
                loanAmt.append(loan_amt)
            else:
                continue

        if len(loanAmt) == 0:
            return 0
        else:
            return max(loanAmt)

    def count_userid_all_max_loan_withdraw_amt_3m(self, id_no):
        '''计算110内部特征变量'''
        loanAmt = []

        # 筛选通道的数据
        channl_value = repay(self.mysql, self.xn, self.env).userid_all_max_loan_withdraw_amt_6m_1(id_no)
        for count_value in channl_value:
            loan_id = count_value['id']
            loan_amt = count_value['loan_principal']
            loan_apply_datetime = str(count_value['loan_date'])
            loan_date = parse(loan_apply_datetime)
            # loan_date = loan_date.strftime('%Y-%m-%d %H:%M:%S')
            date = datetime.datetime.now()
            # now_time = date.strftime('%Y-%m-%d %H:%M:%S')
            count_month = self.get_early_date(date, 3)
            if loan_date >= count_month and loan_date <= date:
                loanAmt.append(loan_amt)
            else:
                continue

        # 筛选实担的数据
        really_value = repay(self.mysql, self.xn, self.env).userid_all_max_loan_withdraw_amt_6m_2(id_no)
        for count_value in really_value:
            loan_id = count_value['id']
            loan_amt = count_value['loan_amt']
            loan_apply_datetime = count_value['cap_interest_day']
            date = datetime.datetime.now()
            # now_time = date.strftime('%Y-%m-%d %H:%M:%S')
            count_month = self.get_early_date(date, 3)

            if loan_apply_datetime >= count_month and loan_apply_datetime <= date:
                loanAmt.append(loan_amt)
            else:
                continue

        if len(loanAmt) == 0:
            return 0
        else:
            return max(loanAmt)

    def count_userid_all_max_loan_withdraw_amt_6m(self, id_no):
        '''计算110内部特征变量'''
        loanAmt = []

        # 筛选通道的数据
        channl_value = repay(self.mysql, self.xn, self.env).userid_all_max_loan_withdraw_amt_6m_1(id_no)
        for count_value in channl_value:
            loan_id = count_value['id']
            loan_amt = count_value['loan_principal']
            loan_apply_datetime = str(count_value['loan_date'])
            loan_date = parse(loan_apply_datetime)
            # loan_date = loan_date.strftime('%Y-%m-%d %H:%M:%S')
            date = datetime.datetime.now()
            # now_time = date.strftime('%Y-%m-%d %H:%M:%S')
            count_month = self.get_early_date(date, 6)
            if loan_date >= count_month and loan_date <= date:
                loanAmt.append(loan_amt)
            else:
                continue

        # 筛选实担的数据
        really_value = repay(self.mysql, self.xn, self.env).userid_all_max_loan_withdraw_amt_6m_2(id_no)
        for count_value in really_value:
            loan_id = count_value['id']
            loan_amt = count_value['loan_amt']
            loan_apply_datetime = count_value['cap_interest_day']
            date = datetime.datetime.now()
            # now_time = date.strftime('%Y-%m-%d %H:%M:%S')
            count_month = self.get_early_date(date, 6)

            if loan_apply_datetime >= count_month and loan_apply_datetime <= date:
                loanAmt.append(loan_amt)
            else:
                continue

        if len(loanAmt) == 0:
            return 0
        else:
            return max(loanAmt)

    def count_userid_all_max_loan_withdraw_amt_12m(self, id_no):
        '''计算111内部特征变量'''
        loanAmt = []

        # 筛选通道的数据
        channl_value = repay(self.mysql, self.xn, self.env).userid_all_max_loan_withdraw_amt_6m_1(id_no)
        for count_value in channl_value:
            loan_id = count_value['id']
            loan_amt = count_value['loan_principal']
            loan_apply_datetime = str(count_value['loan_date'])
            loan_date = parse(loan_apply_datetime)
            # loan_date = loan_date.strftime('%Y-%m-%d %H:%M:%S')
            date = datetime.datetime.now()
            # now_time = date.strftime('%Y-%m-%d %H:%M:%S')
            count_month = self.get_early_date(date, 12)
            if loan_date >= count_month and loan_date <= date:
                loanAmt.append(loan_amt)
            else:
                continue

        # 筛选实担的数据
        really_value = repay(self.mysql, self.xn, self.env).userid_all_max_loan_withdraw_amt_6m_2(id_no)
        for count_value in really_value:
            loan_id = count_value['id']
            loan_amt = count_value['loan_amt']
            loan_apply_datetime = count_value['cap_interest_day']
            date = datetime.datetime.now()
            # now_time = date.strftime('%Y-%m-%d %H:%M:%S')
            count_month = self.get_early_date(date, 12)

            if loan_apply_datetime >= count_month and loan_apply_datetime <= date:
                loanAmt.append(loan_amt)
            else:
                continue

        if len(loanAmt) == 0:
            return 0
        else:
            return max(loanAmt)


    def count_userid_grt_min_loan_withdraw_amt_tot(self, id_no):
        '''计算112内部特征变量'''

        value = repay(self.mysql, self.xn, self.env).userid_grt_min_loan_withdraw_amt_tot(id_no)
        min_value = value[0]['min(loan_amt)']
        return min_value

    def count_userid_all_min_loan_withdraw_amt_tot(self, id_no):
        '''计算113内部特征变量'''
        loanAmt = []

        # 筛选通道的数据
        c_value = repay(self.mysql, self.xn, self.env).userid_all_min_loan_withdraw_amt_tot_1(id_no)

        channl_value = c_value[0]['min(loan_principal)']
        if channl_value is not None:
            loanAmt.append(channl_value)


        # 筛选实担的数据
        r_value = repay(self.mysql, self.xn, self.env).userid_all_min_loan_withdraw_amt_tot_2(id_no)

        really_value = r_value[0]['min(loan_amt)']
        if really_value is not None:
            loanAmt.append(really_value)

        if len(loanAmt) == 0:
            return 0
        else:
            return min(loanAmt)

    def count_userid_psg_loan_withdraw_orgcnt_1m(self, id_no):
        '''计算114内部特征变量'''
        assetOrgNo = []

        channl_value = repay(self.mysql, self.xn, self.env).userid_psg_loan_withdraw_orgcnt_1m(id_no)
        for count_value in channl_value:
            loan_id = count_value['id']

            asset_org_no = count_value['asset_org_no']
            loan_apply_datetime = str(count_value['loan_date'])
            loan_date = parse(loan_apply_datetime)
            # loan_date = loan_date.strftime('%Y-%m-%d %H:%M:%S')
            date = datetime.datetime.now()
            # now_time = date.strftime('%Y-%m-%d %H:%M:%S')
            count_month = self.get_early_date(date, 1)
            if loan_date >= count_month and loan_date <= date:
                assetOrgNo.append(asset_org_no)
        print("assetOrgNo为： %s" % (assetOrgNo, ))

        return len(list(set(assetOrgNo)))

    def count_userid_psg_loan_withdraw_orgcnt_3m(self, id_no):
        '''计算115内部特征变量'''
        assetOrgNo = []

        channl_value = repay(self.mysql, self.xn, self.env).userid_psg_loan_withdraw_orgcnt_1m(id_no)
        for count_value in channl_value:
            loan_id = count_value['id']
            asset_org_no = count_value['asset_org_no']
            loan_apply_datetime = str(count_value['loan_date'])
            loan_date = parse(loan_apply_datetime)
            # loan_date = loan_date.strftime('%Y-%m-%d %H:%M:%S')
            date = datetime.datetime.now()
            # now_time = date.strftime('%Y-%m-%d %H:%M:%S')
            count_month = self.get_early_date(date, 3)
            if loan_date >= count_month and loan_date <= date:
                assetOrgNo.append(asset_org_no)
        print("assetOrgNo为： %s" % (assetOrgNo, ))

        return len(list(set(assetOrgNo)))

    def count_userid_psg_loan_withdraw_orgcnt_6m(self, id_no):
        '''计算116内部特征变量'''
        assetOrgNo = []

        channl_value = repay(self.mysql, self.xn, self.env).userid_psg_loan_withdraw_orgcnt_1m(id_no)
        for count_value in channl_value:
            loan_id = count_value['id']
            asset_org_no = count_value['asset_org_no']
            loan_apply_datetime = str(count_value['loan_date'])
            loan_date = parse(loan_apply_datetime)
            # loan_date = loan_date.strftime('%Y-%m-%d %H:%M:%S')
            date = datetime.datetime.now()
            # now_time = date.strftime('%Y-%m-%d %H:%M:%S')
            count_month = self.get_early_date(date, 6)

            if loan_date >= count_month and loan_date <= date:
                assetOrgNo.append(asset_org_no)
        print("assetOrgNo为： %s" % (assetOrgNo, ))

        return len(list(set(assetOrgNo)))

    def count_userid_psg_loan_withdraw_orgcnt_12m(self, id_no):
        '''计算117内部特征变量'''
        assetOrgNo = []

        channl_value = repay(self.mysql, self.xn, self.env).userid_psg_loan_withdraw_orgcnt_1m(id_no)
        for count_value in channl_value:
            loan_id = count_value['id']
            asset_org_no = count_value['asset_org_no']
            loan_apply_datetime = str(count_value['loan_date'])
            loan_date = parse(loan_apply_datetime)
            # loan_date = loan_date.strftime('%Y-%m-%d %H:%M:%S')
            date = datetime.datetime.now()
            # now_time = date.strftime('%Y-%m-%d %H:%M:%S')
            count_month = self.get_early_date(date, 12)

            if loan_date >= count_month and loan_date <= date:
                assetOrgNo.append(asset_org_no)
        print("assetOrgNo为： %s" % (assetOrgNo, ))

        return len(list(set(assetOrgNo)))

    def count_userid_self_prod_15d_settle_terms_tot(self, id_no):
        '''inner_feature_0024'''
        billId = []
        channl_value = repay(self.mysql, self.xn, self.env, self.asset_org_no, self.bis_type_id).userid_self_prod_15d_settle_terms_tot_1(id_no)
        for count_value in channl_value:
            loan_order_id = count_value['id']
            cap_interest_day = str(count_value['cap_interest_day'])[0:10]
            loan_period = count_value['loan_period']
            repay_value = repay(self.mysql, self.xn, self.env).userid_self_prod_15d_settle_terms_tot_2(loan_period, loan_order_id)
            for count_repay_value in repay_value:
                last_rpy_datetime = str(count_repay_value['last_rpy_datetime'])[0:10]
                if self.compare_time(cap_interest_day, last_rpy_datetime) + 1 <= 15:
                    repay_bill = repay(self.mysql, self.xn, self.env).userid_self_prod_15d_settle_terms_tot_3(loan_order_id)
                    for bill in repay_bill:
                        bill_id = bill['id']
                        billId.append(bill_id)
                else:
                    continue

        return len(list(set(billId)))

    def count_userid_self_prod_last_loan_withdraw_date(self, id_no):
        '''inner_feature_0012'''

        time = repay(self.mysql, self.xn, self.env, self.asset_org_no, self.bis_type_id).userid_userid_self_prod_last_loan_withdraw_date(id_no)

        max_time = time[0]['max(cap_interest_day)']
        return max_time


if __name__ == '__main__':
    mysql = "adb"
    xn = "dw"
    env = "test1"
    # CI2202110000800134, CI2202110000800137
    id_no = "CI2202110000800137"
    asset_org_no ="360JR"
    bis_type_id = "0001"
    max_loan_amt = repay_count(mysql, xn, env, asset_org_no, bis_type_id).count_userid_psg_loan_withdraw_orgcnt_12m(id_no)
    print("count_prod_ever_overdue_cnt_tot的值为：%s" % (max_loan_amt, ))







