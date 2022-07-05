# -*- coding: utf-8 -*-

# @Time : 2022/5/6 17:06

# @Author : WangJun

# @File : channl_repay.py

# @Software: PyCharm
import datetime
import os
import time
import paramiko
import string
from common.conn_config import *
from common.date_encoder import *
from database.update_pls_plan import *
import requests
import random
s = requests.Session()

class channl:
    def __init__(self, mysql, xn, env: str,  loan_term, id, loanAmt, project_no, assert_no, re_term=1):

        if env == "test1":
            self.url = "http://172.16.11.93:8717"
        elif env == "test2":
            self.url = "http://172.16.11.118:8717"
        elif env == "comb":
            self.url = "http://172.16.11.102:8717"
        self.mysql = mysql
        self.xn = xn
        self.project_no = project_no
        self.assert_no = assert_no

        # self.linux_dir = "/sftp/xna/lexin/upload/lexin/20211226/"

        self.env = env
        self.loan_term = loan_term
        self.re_term = re_term
        self.id = id
        self.loanAmt = loanAmt
        self.headers = {
            "Content-Type": "application/json",
            "isTest_post": "true",
            'Connection': 'close'
        }
        self.idCard = []


    def now_time(self, time):
        # re = datetime.datetime.now().__format__('%Y-%m-%d %H:%M:%S')
        re = time.split(' ')
        re = re[0].split('-')
        re = re[0] + re[1] + re[2]
        return re

    def random_param(self):
        param1 = ''.join(str(i) for i in random.sample(string.digits, 8))
        param2 = ''.join(str(i) for i in random.sample(range(0, 9), 9))
        param3 = str(random.randint(0, 9))
        projece_c = 'XNAP' + param2 + param1 + param3

        return projece_c

    def repay(self, order_no:str, repay_time, cap_repay_interest=0, cap_repay_overdue_interest=0, repay_type="01", repayAmt=''):
        url = self.url + "/yht-front-oms/api/pushData"
        loanAmt = round((self.loanAmt / self.loan_term), 2)

        j = 1
        repay_record_data = []
        for i in range(self.re_term):

            # c_time = datetime.datetime.strftime(repay_time[i], '%Y-%m-%d %H:%M:%S')
            c_time = self.now_time(repay_time[i])

            record = {
                "orderNo": order_no,
                "repayRecordId": self.random_param(),
                "repayDate": c_time,
                "repayPrincipal": repayAmt,
                "repayInterest": str(cap_repay_interest),
                "repayGuaranteeFee": "10",
                "repayLateFee": "4",
                "repayOverdueInterest": str(cap_repay_overdue_interest),
                "repayType": repay_type,
                "repayNper": str(j),
                "repayOtherFee": "7",
                "breaksFee": "8",
                "repayPrice": "9"

            }
            repay_record_data.append(record)
            plan(self.mysql, self.xn, self.env).update_pls_plan(str(loanAmt), str(cap_repay_interest),
                                                                str(cap_repay_overdue_interest), repay_type, c_time,
                                                                order_no, str(j))
            settled_status = plan(self.mysql, self.xn, self.env).pls_plan_record(order_no, str(j))

            settled = settled_status['order_no']
            if settled is not None:
                settled_sign = 'Y'
            else:
                settled_sign = 'N'
            plan(self.mysql, self.xn, self.env).updates_pls_plan(settled_sign, order_no, str(j))


            record_data = {
                "merchantNo": self.assert_no,
                "projectNo": self.project_no,
                "dataType": "PR",
            }
            record_data['data'] = repay_record_data

            print("第%d期---------" %(i,))
            record_response = requests.post(url=url, data=json.dumps(record_data), headers=self.headers)
            if record_response.status_code == 200:
                print("第%d期还款成功" %(j, ))
            j += 1


if __name__ == '__main__':
    # print(channel().identity_card())
    # zzx-lx-qnyh TDB01
    mysql = 'jly'
    assert_no = 'xiaohua'
    project_no = "zzx-xh-lzyh"
    # 融担环境
    xn = "xna"
    # 环境
    env = "test1"
    # 借款期数，用来生成还款计划
    loan_term = 3
    # 还款期数，用来生成还款记录
    re_term = 1
    # 借款金额
    loanAmt = 300
    # 还款金额
    repayAmt = '100'
    id = "110101195107073112"
    # 资金方利息
    cap_repay_interest = 10
    # 资金方罚息
    cap_repay_overdue_interest = 0
    # 还款类型 01-正常还款 02-提前结清, 03-提前还款
    repay_type = "01"
    # 订单号
    order_no = "orderEIMXOQya7306529453241709g3"
    repay_time = ["2021-12-25 01:00:00", "2022-01-25 01:00:00", "2022-02-25 01:00:00"]
    # loan_term:借款期限 re_term：还款期数
    main_plan = channl(mysql=mysql, xn=xn, env=env, loan_term=loan_term, id=id, loanAmt=loanAmt,
                       project_no=project_no, assert_no=assert_no, re_term=re_term)

    main_plan.repay(order_no=order_no, repay_time=repay_time, cap_repay_interest=cap_repay_interest,
                    cap_repay_overdue_interest=cap_repay_overdue_interest, repay_type=repay_type, repayAmt=repayAmt)

