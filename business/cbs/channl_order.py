# -*- coding: utf-8 -*-

# @Time : 2022/3/11 11:56

# @Author : WangJun

# @File : channl_order.py

# @Software: PyCharm
import requests
import json
import random

import datetime
import os
import time
import paramiko
import string
from common.conn_config import *
from common.date_encoder import *
from database.update_pls_plan import *
s = requests.Session()

class channel:

    def __init__(self, mysql,xn, env:str, custName:str, loan_term, id, loanAmt, project_no, assert_no,re_term=1):

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

        self.cust_name = custName
        self.s = requests.Session()


    def login(self):
        '''登录'''
        data = {
            "uname": "risk",
            "pwd": "risk@2021&&"
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        url = "https://oms{}.jiuliyuntech.com/sso-oms/loginByAjax".format(self.env)

        response = self.s.post(url=url, data=data, headers=headers).json()

        print(response["msg"])


    # def ex_scheduler2(self):
    #     if self.env == 'test1':
    #         jobid= 'pls-046'
    #     else:
    #         jobid = 'pls-027'
    #     data1 = {
    #         "jobid": jobid,
    #         "executeTime": self.now_time()
    #
    #     }
    #     headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
    #
    #     url = 'https://oms{}.jiuliyuntech.com/scheduler-oms/job/execute'.format(self.env)
    #     response = self.s.post(url=url, data=data1, headers=headers)
    #     if response.status_code == 200:
    #         print("执行还款记录入账到还款计划成功")

    def re_time(self):
        re = datetime.datetime.now().__format__('%Y-%m-%d %H:%M:%S')
        re = time.strptime(re, "%Y-%m-%d %H:%M:%S")
        re = int(time.mktime(re))
        re = str(re)

        return re

    def monthdelta(self,date, delta):
        m, y = (date.month + delta) % 12, date.year + ((date.month) + delta - 1) // 12
        if not m: m = 12
        d = min(date.day, [31,
                           29 if y % 4 == 0 and not y % 400 == 0 else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][
            m - 1])
        return date.replace(day=d, month=m, year=y)

    def r_time(self,time, loan_trem):
        list = []
        now = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
        for i in range(loan_trem + 1):
            re = self.monthdelta(now, i)
            re = re.__format__('%Y-%m-%d %H:%M:%S')
            re = re.split(' ')
            re = re[0].split('-')
            re = re[0] + re[1] + re[2]
            list.append(re)

        del list[0]

        return list

    def now_time(self, time):
        # re = datetime.datetime.now().__format__('%Y-%m-%d %H:%M:%S')
        re = time.split(' ')
        re = re[0].split('-')
        re = re[0] + re[1] + re[2]
        return re

    def c_now_time(self):
        re = datetime.datetime.now().__format__('%Y-%m-%d %H:%M:%S')
        re = re.split(' ')
        re = re[0].split('-')
        re = re[0] + re[1] + re[2]
        return re

    def n_time(self):
        re = (datetime.datetime.now() - datetime.timedelta(days=1)).__format__('%Y-%m-%d %H:%M:%S')
        re = re.split(' ')
        re = re[0].split('-')
        re = re[0] + re[1] + re[2]

        return re

    def random_param(self):
        param1 = ''.join(str(i) for i in random.sample(string.digits, 8))
        param2 = ''.join(str(i) for i in random.sample(range(0, 9), 9))
        param3 = str(random.randint(0, 9))
        projece_c = 'XNAP' + param2 + param1 + param3

        return projece_c

    # 代偿接口
    def compensatory(self, order_n, term, compensateDate):
        orders_n = ''.join(random.sample(string.ascii_letters, 8))
        number = ''.join(random.sample(string.digits, 8))
        compensateRecordId = "XNAP" + orders_n + number + number
        url = self.url + "/yht-front-oms/api/pushData"
        time = int(self.n_time())
        data = {
            "merchantNo": self.assert_no,
            "projectNo": self.project_no,
            "dataType": "CPI",
            "data": [
                {
                    "orderNo": order_n,
                    "compensateRecordId": compensateRecordId,
                    "compensatePrincipal": "1",
                    "compensateInterest": "2",
                    "compensateOverdueInterest": "3",
                    "compensateGuaranteeFee": "4",
                    "compensateFee": "5",
                    "compensateDate": compensateDate,
                    "compensateTotalAmt": "7",
                    "term": term,
                    "compensateType": "02"
                }
            ]
        }
        response = requests.post(url=url, data=json.dumps(data), headers=self.headers)

        return response.text

    # 还款计划和还款记录
    def repay_plan(self, time, order_no:str,compensatory_time, repay_status, cap_repay_interest=0, cap_repay_overdue_interest=0, repay_type="01", repayAmt='', compensatory_day=0):
        plan_data = []
        rt = self.re_time()
        re = self.r_time(time, self.loan_term)
        i = 1
        loanAmt = round((self.loanAmt/self.loan_term), 2)
        # print(loanAmt)
        for j in re:
            plan_param = {

                "orderNo": order_no,
                "nper": str(i),
                "needRepayDate": j,
                "needRepayPrincipal": str(loanAmt),
                "needRepayInterest": str(cap_repay_interest),
                "needRepayServiceFee": "0.00",
                "lateFee": "0.00",
                "overdueInterest": "0.00",
                "otherFee": "0.00",
                "needRepayGuaranteeFee": "0.00",
                "repayPrincipal": "0.00",
                "repayInterest": "0.00",
                "repayServiceFee": "0.00",
                "repayLateFee": "0.00",
                "repayOverdueInterest": "0.00",
                "repayOtherFee": "0.00",
                "repayGuaranteeFee": "0.00",
                "overdueSign": "N",
                "settledSign": "N",
                "lastRepayDate": ""

            }
            plan_data.append(plan_param)
            i += 1

        url = self.url + "/yht-front-oms/api/pushData"

        plans_data = {
            "merchantNo": self.assert_no,
            "projectNo": self.project_no,
            "dataType": "PS"
        }
        plans_data['data'] = plan_data
        # print(json.dumps(plans_data, cls=DateEncoder, ensure_ascii=False))
        plan_response = requests.post(url=url, data=json.dumps(plans_data), headers=self.headers)
        # print(plan_response)

        if repay_status == "true":
            repay_record_data = []

            j = 1
            for i in range(self.re_term):
                record = {
                    "orderNo": order_no,
                    "repayRecordId": self.random_param(),
                    "repayDate": re[i],
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
                                                                    str(cap_repay_overdue_interest), repay_type, re[i],
                                                                    order_no, str(j))
                settled_status = plan(self.mysql, self.xn, self.env).pls_plan_record(order_no, str(j))

                settled = settled_status['order_no']
                if settled is not None:
                    settled_sign = 'Y'
                else:
                    settled_sign = 'N'
                plan(self.mysql, self.xn, self.env).updates_pls_plan(settled_sign, order_no, str(j))
                j += 1

            record_data = {
                "merchantNo": self.assert_no,
                "projectNo": self.project_no,
                "dataType": "PR",
            }
            record_data['data'] = repay_record_data
            record_response = requests.post(url=url, data=json.dumps(record_data), headers=self.headers)

        # 代偿逻辑
        compensatory_record_time = []
        compensatory_record = plan(self.mysql, self.xn, self.env).query_pls_plan(order_no)
        # last_repay_date = compensatory_record['compensatory_record']
        for record in compensatory_record:
            need_repay_date = record['need_repay_date']

            need_repay_date = str(need_repay_date)
            need_repay_date = "{}-{}-{} 00:00:00".format(need_repay_date[0:4], need_repay_date[4:6], need_repay_date[6:])
            n_repay_date = datetime.datetime.strptime(need_repay_date, '%Y-%m-%d %H:%M:%S')
            c_time = n_repay_date + datetime.timedelta(days=compensatory_time)
            c_time = datetime.datetime.strftime(c_time, '%Y-%m-%d %H:%M:%S')
            c_time = self.now_time(c_time)
            nper = record['nper']
            compensatory = int(nper-1)
            compensatory_date = re[compensatory]
            if need_repay_date is not None and nper is not None:
                now_time = self.c_now_time()
                if now_time >= c_time:
                    self.compensatory(order_no, nper, c_time)
                    compensatory_record_time.append(c_time)
            else:
                continue

        # repay_time = self.r_time(time, self.loan_term)
        if compensatory_day != 0:
            repay_record_data = []

            j = 1

            for i in range(len(compensatory_record_time)):

                record_time = compensatory_record_time[i]

                record_time = "{}-{}-{} 00:00:00".format(record_time[0:4], record_time[4:6],
                                                             record_time[6:])
                record_time = datetime.datetime.strptime(record_time, '%Y-%m-%d %H:%M:%S')
                c_time = record_time + datetime.timedelta(days=compensatory_day)
                c_time = datetime.datetime.strftime(c_time, '%Y-%m-%d %H:%M:%S')
                c_time = self.now_time(c_time)
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
                j += 1

            record_data = {
                "merchantNo": self.assert_no,
                "projectNo": self.project_no,
                "dataType": "PR",
            }
            record_data['data'] = repay_record_data
            record_response = requests.post(url=url, data=json.dumps(record_data), headers=self.headers)


    def push_custData(self, time, compensatory_time, repay_status, cap_repay_interest=0, cap_repay_overdue_interest=0, repay_type="01",repayAmt='',compensatory_day=0):
        '''推送客户信息'''
        url = self.url + "/yht-front-oms/api/pushData"
        # # id_card = self.identity_card()
        # self.idCard.append(id_card)
        sex = random.choice([0, 1])
        order_n = ''.join(random.sample(string.ascii_letters, 8))
        number = ''.join(random.sample(string.digits, 8))
        number_1 = ''.join(random.sample(string.digits, 8))
        od_n = "order" + order_n + number + number_1 + "g3"

        loan_date = datetime.datetime.now().__format__('%Y-%m-%d %H:%M:%S')

        data = {
            "merchantNo": self.assert_no,
            "projectNo": self.project_no,
            "dataType": "OCI",
            "data": [
                {
                    "orderNo": od_n,
                    "idCardNo": self.id,
                    "custName": self.cust_name,
                    "loanDate": self.now_time(time),
                    "loanNper": self.loan_term,
                    "loanPrincipal": self.loanAmt,
                    "financingPartner": 0,
                    "annualInterestRate": 1.23456,
                    "fundLoanInterestRate": 0.123456,
                    "penaltyInterestRate": 0.123456,
                    "fundPenaltyInterestRate": 0.123456,
                    "repayWay": "01",
                    "productType": "产品类型A",
                    "fixedBillDay": 10,
                    "fixedRepayDay": 3,
                    "loanUse": "其他",
                    "openAcctName": "银行卡账户名XN_360",
                    "bankCardNo": 6217002020039336,
                    "custName": self.cust_name,
                    "idCardNo": self.id,
                    "userSex": sex,
                    "nation": "汉族",
                    "birthdate": "19930601",
                    "mobileNo": "13783719387",
                    "idCardAddress": "广东省深圳市",
                    "address": "深圳市南山区",
                    "email": "13783719387@163.com",
                    "idIssueDate": "20200101",
                    "idExpireDate": "20300101",
                    "idCardOrganization": "asd",
                    "region": "1"
                }
            ]
        }

        response = requests.post(url=url, data=json.dumps(data), headers=self.headers, verify=False)

        if response.status_code == 200:
            print("发送订单成功，订单号为: %s" % (od_n,))
            self.repay_plan(time, od_n, compensatory_time, repay_status,cap_repay_interest, cap_repay_overdue_interest, repay_type, repayAmt,compensatory_day)
            # self.login()
            # for i in range(1):
            #
            #     self.ex_scheduler2()

        else:
            print("调用异常，推送数据失败")

    def test_result(self, future):
        future.result()

    def main(self,thread,time, compensatory_time, repay_status, cap_repay_interest=0, cap_repay_overdue_interest=0, repay_type="01",repayAmt='',compensatory_day=0):
        from concurrent.futures import ThreadPoolExecutor
        threadPool = ThreadPoolExecutor(max_workers=4, thread_name_prefix="test_")
        for i in range(thread):
            future = threadPool.submit(self.push_custData, time, compensatory_time, repay_status,cap_repay_interest,
                                       cap_repay_overdue_interest, repay_type, repayAmt,compensatory_day)
            future.add_done_callback(self.test_result)

        threadPool.shutdown(wait=True)
        print('main finished')


if __name__ == '__main__':
    # print(channel().identity_card())
    # zzx-lx-qnyh TDB01
    mysql = 'jly'
    assert_no = 'juzi'
    project_no = "qhhf-juzi-lzyh"
    # 融担环境
    xn = "xnb"
    # 环境
    env = "test1"
    # 借款时间
    loan_time = "2021-11-25 01:00:00"
    # 代偿天数
    compensatory_time = 20
    # 客户姓名
    cust_name = "汪离15"
    # 借款期数，用来生成还款计划
    loan_term = 3
    # 还款期数，用来生成还款记录
    re_term = 2
    # 借款金额
    loanAmt = 300
    # 还款金额
    repayAmt = '100'
    id = "110101196103079052"
    # 资金方利息
    cap_repay_interest = 10
    # 资金方罚息
    cap_repay_overdue_interest = 0
    # 还款类型 01-正常还款 02-提前结清, 03-提前还款
    repay_type = "01"
    # true为还款，false为不还款
    repay_status = "false"
    # 代偿后还款间隔，等于0时表示代偿后不还款
    compensatory_day = 2
    # 线程数
    thread = 1
    # loan_term:借款期限 re_term：还款期数
    main_plan = channel(mysql=mysql, xn=xn, env=env, custName=cust_name, loan_term=loan_term, id=id,
                   loanAmt=loanAmt, project_no=project_no, assert_no=assert_no, re_term=re_term)

    main_plan.main(thread=thread, time=loan_time, compensatory_time=compensatory_time, repay_status=repay_status, cap_repay_interest=cap_repay_interest,
              cap_repay_overdue_interest=cap_repay_overdue_interest, repay_type=repay_type,repayAmt=repayAmt, compensatory_day=compensatory_day)


