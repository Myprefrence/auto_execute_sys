import requests
import json
import random

import datetime
import os
import time
import paramiko
import string
from common.conn_config import *


class channel:

    def __init__(self, xn, env:str, custName:str, loan_term, id, loanAmt, project_no, re_term=1):

        if env == "test1":
            self.url = "http://172.16.11.93:8717"
        elif env == "test2":
            self.url = "http://172.16.11.118:8717"
        elif env == "comb":
            self.url = "http://172.16.11.102:8717"
        self.red_re = read_config()
        if env == "test1":
            self.linux_url = "172.16.11.93"
            self.user = self.red_re.read_project("Test1", "user")
            self.password = self.red_re.read_project("Test1", "password")
        elif env == "test2":
            self.linux_url = "172.16.11.118"
            self.user = self.red_re.read_project("Test2", "user")
            self.password = self.red_re.read_project("Test2", "password")

        self.root_dir = os.path.dirname(os.path.abspath('..'))

        self.xn = xn
        self.project_no = project_no

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
        headers = {"Content-Type": "application/x-www-form-urlencoded",'Connection': 'close'}
        url = "https://oms{}.jiuliyuntech.com/sso-oms/loginByAjax".format(self.env)

        response = self.s.post(url=url, data=data, headers=headers).json()

        print(response["msg"])

    def del_file(self, path):
        ls = os.listdir(path)
        for i in ls:
            c_path = os.path.join(path, i)
            if os.path.isdir(c_path):
                self.del_file(c_path)
            else:
                os.remove(c_path)

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

    def r_time(self, loan_trem):
        list = []
        now = datetime.datetime.now()
        for i in range(loan_trem + 1):
            re = self.monthdelta(now, i)
            re = re.__format__('%Y-%m-%d %H:%M:%S')
            re = re.split(' ')
            re = re[0].split('-')
            re = re[0] + re[1] + re[2]
            list.append(re)

        del list[0]

        return list

    def now_time(self):
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

    def wirte_repayment_plan(self, order_no:str,cap_repay_interest=0,cap_repay_overdue_interest=0,
                             reality_capital=0, reality_interest=0, reality_overdue_interest=0, repay_type="10"):
        '''生成还款计划文件'''
        rt = self.re_time()
        re = self.r_time(self.loan_term)
        #还款计划文件
        rp_file = self.root_dir + r'\config\re_config\repayment_plan_' + rt + '.txt'
        rp_ok_file = self.root_dir + r'\config\re_config\repayment_plan_' + rt + '.ok'
        #还款文件
        rm_file = self.root_dir + r'\config\re_config\repayment_' + rt + '.txt'
        rm_ok_file = self.root_dir + r'\config\re_config\repayment_' + rt + '.ok'

        dir = self.root_dir + r'\config\re_config'
        self.del_file(dir)

        i = 1
        loanAmt = round((self.loanAmt/self.loan_term), 2)
        # print(loanAmt)
        for j in re:

            param = order_no + '|||' + str(i) + '|' + str(loanAmt) + '||' + j + '|12.44|0.12|10|'

            with open(rp_file, 'a', encoding='utf-8') as f:
                f.write(param + '\n')

            with open(rp_ok_file, 'a', encoding='utf-8') as f_ok:
                f_ok.write(param + '\n')

            i += 1
        f.close()
        f_ok.close()

        j = 1
        for i in range(self.re_term):
            param = order_no + "||" + str(
                j) + "|" + str(loanAmt) + "|" + str(cap_repay_interest) + "|" + str(cap_repay_overdue_interest) + \
                    "|" + str(reality_capital) + "|" + str(reality_interest) + "|" + str(reality_overdue_interest) + \
                    "|1.39|" + repay_type + "||||1.23|" + re[i] + \
                    "|" + self.random_param() + "|"
            # for js in re:


            with open(rm_file, 'a', encoding='utf-8') as rm:
                    rm.write(param + '\n')

            with open(rm_ok_file, 'a', encoding='utf-8') as rm_ok:
                    rm_ok.write(param + '\n')

            j += 1
            rm.close()
            rm_ok.close()

        return rp_file, rp_ok_file, rm_file, rm_ok_file

    def exec_cmd(self,cmd):
        host = self.linux_url
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #ssh.connect(hostname, port, username, password, pkey, key_filename, timeout, allow_agent, look_for_keys, compress, sock)
        ssh.connect(host, 22, self.user, self.password)
        stdin,stdout,stderr = ssh.exec_command(cmd)
        # print(stdout.readlines())
        ssh.close()

    def downfile(self,remotepath,localpath):

        host = self.linux_url
        t = paramiko.Transport(host, 22)
        t.connect(username=self.user, password=self.password)
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.get(remotepath,localpath)
        t.close()

    def upload_file(self):
        # ssh = paramiko.SSHClient()
        # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # ssh.connect('')
        # a, b, c = ssh.exec_command('')
        # info = b.read().decode('utf-8')
        # print(info)
        host = self.linux_url
        t = paramiko.Transport(host, 22)
        t.connect(username=self.user, password=self.password)
        p = paramiko.SFTPClient.from_transport(t)
        rootdir = self.root_dir + r'\config\re_config'
        n_time = self.n_time()
        # linux项目路径
        if self.xn == "xnb":
            liunx_d = read_config().read_project("LeXin", "linux_dir_xnb")
        else:
            liunx_d = read_config().read_project("LeXin", "linux_dir_xna")
        cmd = "mkdir -p " + liunx_d + str(n_time)
        self.exec_cmd(cmd)
        time.sleep(0.5)
        linux_dirs = liunx_d + str(n_time) + "/"
        list = os.listdir(rootdir)
        for i in range(0, len(list)):
            path = os.path.join(rootdir, list[i])
            split_path = path.split("\\")
            linux_dir = linux_dirs + split_path[5]
            p.put(path, linux_dir)

    def ex_scheduler(self):
        url = 'https://oms{}.jiuliyuntech.com/scheduler-oms/job/execute'.format(self.env)
        data = {
            "jobid": "pls-014",
            "executeTime": self.now_time()
        }

        headers = {"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",'Connection': 'close'}

        response = self.s.post(url=url, data=data, headers=headers)
        if response.status_code == 200:
            print("执行sftp文件定时拉取机构数据任务成功")

    def ex_scheduler1(self):
        data1 = {
            "jobid": "pls-013",
            "executeTime": self.now_time()

        }
        headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",'Connection': 'close'}

        url = 'https://oms{}.jiuliyuntech.com/scheduler-oms/job/execute'.format(self.env)
        response = self.s.post(url=url, data=data1, headers=headers)
        if response.status_code == 200:
            print("执行sftp解析机构数据任务成功")

    def ex_scheduler2(self):
        if self.env == 'test1':
            jobid= 'pls-046'
        else:
            jobid = 'pls-027'
        data1 = {
            "jobid": jobid,
            "executeTime": self.now_time()

        }
        headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", 'Connection': 'close'}

        url = 'https://oms{}.jiuliyuntech.com/scheduler-oms/job/execute'.format(self.env)
        response = self.s.post(url=url, data=data1, headers=headers)
        if response.status_code == 200:
            print("执行还款记录入账到还款计划成功")

    # def identity_card(self):
    #     """提取身份证号码"""
    #     url = "http://172.16.9.77:7300/mock/600e8061e319a76092523653/common/data"
    #     headers = {"Content-Type": "application/json", 'Connection': 'close'}
    #     data = {}
    #     response = requests.post(url=url, data=json.dumps(data), headers=headers).json()
    #
    #     if response != None:
    #         idCard = response["idCard"]
    #
    #     else:
    #         print("接口调用异常！！！")
    #
    #     return idCard

    def compensatory(self, order_n):
        orders_n = ''.join(random.sample(string.ascii_letters, 8))
        number = ''.join(random.sample(string.digits, 8))
        compensateRecordId = "XNAP" + orders_n + number + number
        url = self.url + "/yht-front-oms/api/pushData"
        time = int(self.n_time())
        data = {
            "merchantNo": "LeXin",
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
                    "compensateDate": time,
                    "compensateTotalAmt": "7"
                }
            ]
        }
        response = requests.post(url=url, data=json.dumps(data), headers=self.headers)

        return response.text


    def push_custData(self,cap_repay_interest=0,cap_repay_overdue_interest=0,
                             reality_capital=0, reality_interest=0, reality_overdue_interest=0, repay_type="10"):
        '''推送客户信息'''
        url = self.url + "/yht-front-oms/api/pushData"
        # # id_card = self.identity_card()
        # self.idCard.append(id_card)
        sex = random.choice([0, 1])
        order_n = ''.join(random.sample(string.ascii_letters, 8))
        number = ''.join(random.sample(string.digits, 8))
        od_n = "order" + order_n + number + "g3"


        loan_date = datetime.datetime.now().__format__('%Y-%m-%d %H:%M:%S')

        data = {
            "merchantNo": "LeXin",
            "projectNo": self.project_no,
            "dataType": "OCI",
            "data": [
                {
                    "orderNo": od_n,
                    "idCardNo": self.id,
                    "custName": self.cust_name,
                    "loanDate": self.now_time(),
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

        response = requests.post(url=url, data=json.dumps(data), headers=self.headers,verify=False)

        if response.status_code == 200:
            print("发送订单成功，订单号为: %s" % (od_n,))
            self.wirte_repayment_plan(od_n, cap_repay_interest, cap_repay_overdue_interest,
                             reality_capital, reality_interest, reality_overdue_interest, repay_type)
            time.sleep(1)
            self.upload_file()
            self.login()
            for i in range(1):
                self.ex_scheduler()
                time.sleep(2)
                self.ex_scheduler1()
                time.sleep(2)
                self.ex_scheduler2()

            self.compensatory(od_n)
        else:
            print("调用异常，推送数据失败")


if __name__ == '__main__':

    # print(channel().identity_card())
    # zzx-lx-qnyh TDB01
    project_no = "zzx-lx-qnyh"
    #融担环境
    xn = "xna"
    #环境
    env = "test2"
    #客户姓名
    cust_name = "汪离15"
    #借款期数，用来生成还款计划
    loan_term = 3
    #还款期数，用来生成还款记录
    re_term = 2
    #借款金额
    loanAmt = 100
    id = "110101196103079052"
    #资金方利息
    cap_repay_interest = 10
    #资金方罚息
    cap_repay_overdue_interest = 0
    #还款类型 10-正常还款 30-提前结清, 40-逾期还款 50-代偿  100-追偿还款
    repay_type = "10"
    # loan_term:借款期限 re_term：还款期数
    main = channel(xn=xn, env=env, custName=cust_name, loan_term=loan_term, id=id,
                   loanAmt=loanAmt, project_no=project_no, re_term=re_term)

    main.push_custData(cap_repay_interest=cap_repay_interest, cap_repay_overdue_interest=cap_repay_overdue_interest,
                       repay_type=repay_type)

    # print(main.compensatory('orderbTFPMQvt39624018g3'))









