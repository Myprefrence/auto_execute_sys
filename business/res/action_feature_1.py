# -*- coding: utf-8 -*-

# @Time : 2022/1/25 10:29

# @Author : WangJun

# @File : action_feature_1.py

# @Software: PyCharm

from numpy import *

from database.query_action import *
from numpy import *
import time
import datetime


class ActionFeatures:

    def __init__(self, mysql, env, id_no, asset_org_no='', bis_type_id='', project_no=[]):

        self.xn = ["xna", "xnb"]
        self.env = env
        self.id_no = id_no
        self.asset_org_no = asset_org_no
        self.bis_type_id = bis_type_id
        self.project_no = project_no
        self.mysql = mysql



    def count_feature_50(self):
        ''' 统计userid_psg_groupa_max_overdue_days最大逾期天数 '''
        count_max_overdue_day = []
        for xn in self.xn:
            for pn in self.project_no:
                count_repay_settle_1 = Action(self.mysql,xn, self.env).query_action_50_1(self.id_no, pn)

                if count_repay_settle_1 is None:
                    pass

                else:
                    count_max_overdue_day.append(count_repay_settle_1)

                count_repay_settle_0 = Action(self.mysql, xn, self.env).query_action_50_0(self.id_no, pn)

                if count_repay_settle_0 is None:
                    pass

                else:
                    count_max_overdue_day.append(count_repay_settle_0)

        try:
            value = max(count_max_overdue_day)
            return value

        except Exception as e:
            print("未取到值")

    def count_feature_51(self):
        ''' 统计userid_self_prod_actualrepay_amt_tot总实还款金额 '''
        count_amt_tot = []
        for xn in self.xn:

            count_repay = Action(self.mysql, xn, self.env, self.asset_org_no, self.bis_type_id).query_action_51(self.id_no)
            if count_repay is None:
                pass
            else:
                count_amt_tot.append(count_repay)

        value = sum(count_amt_tot)

        return value

    def count_feature_52(self):
        ''' 统计userid_grt_actualrepay_amt_tot总实还款金额 '''
        count_amt_tot = []
        for xn in self.xn:

            count_repay = Action(self.mysql, xn, self.env).query_action_52(self.id_no)
            if count_repay is None:
                pass
            else:
                count_amt_tot.append(count_repay)

        value = sum(count_amt_tot)

        return value

    def count_feature_54(self):
        ''' 统计userid_self_prod_actualrepay_mths_tot统计自然月的还款金额大于0的实还款月 '''
        count_amt_tot = []
        for xn in self.xn:

            count_repay = Action(self.mysql, xn, self.env, self.asset_org_no, self.bis_type_id).query_action_54(self.id_no)
            if count_repay is None:
                pass
            else:
                count_amt_tot.append(count_repay)

        value = sum(count_amt_tot)

        return value

    def count_feature_55(self):
        ''' 统计userid_self_prod_actualrepay_mths_tot统计自然月的还款金额大于0的实还款月 '''
        count_amt_tot = []
        for xn in self.xn:

            count_repay_0 = Action(self.mysql, xn, self.env).query_action_55_0(self.id_no)
            if count_repay_0 is None:
                pass
            else:
                for i in count_repay_0:
                    count_amt_tot.append(i)

            count_repay_1 = Action(self.mysql, xn, self.env).query_action_55_1(self.id_no)
            if count_repay_1 is None:
                pass
            else:
                for j in count_repay_1:
                    count_amt_tot.append(j)

        value = len(list(set(count_amt_tot)))

        return value

    def count_feature_56(self):
        '''特征变量56计算project_line=‘passage’的项目的放款金额'''
        count_amt_tot = []
        for xn in self.xn:

            count_loan_principal = Action(self.mysql, xn, self.env).query_action_56(self.id_no)
            if count_loan_principal is None:
                pass
            else:
                count_amt_tot.append(count_loan_principal)

        value = sum(count_amt_tot)

        return value

    def count_feature_58(self):
        '''特征变量58统计project_line=‘passage’的项目的放款成功的资产方编号'''
        count_amt_tot = []
        for xn in self.xn:

            count_loan_principal = Action(self.mysql, xn, self.env).query_action_58(self.id_no)
            if count_loan_principal is None:
                pass
            else:
                count_amt_tot.append(count_loan_principal)

        value = sum(count_amt_tot)

        return value

    def count_feature_59(self):
        '''特征变量59统计project_line=‘guarantee’的项目的放款成功的最大放款金额'''
        count_amt_tot = []
        for xn in self.xn:

            count_loan_principal = Action(self.mysql, xn, self.env).query_action_59(self.id_no)
            if count_loan_principal is None:
                pass
            else:
                count_amt_tot.append(count_loan_principal)
        try:

            value = max(count_amt_tot)
            return value

        except Exception as e:
            print("未取到值")


if __name__ == '__main__':
    mysql = "jly"
    env = "test1"
    id_no = "110101197903077957"
    asset_org_no = "360JR"
    bis_type_id = "0001"
    project_no = ['ZZX-FENGTAI-LZ', 'zzxyqgdh202101', 'zzxftzb202012', 'zzx-lx-qnyh', 'zzxhx202012',
                  'zzxsnzb202011', 'zzxsnhh202011']
    actionFeature = ActionFeatures(mysql=mysql, env=env, id_no=id_no, asset_org_no=asset_org_no, bis_type_id=bis_type_id,
                                  project_no=project_no)
    print(actionFeature.count_feature_58())

