# -*- coding: utf-8 -*-

# @Time : 2022/2/21 10:57

# @Author : WangJun

# @File : assert_monitor.py

# @Software: PyCharm
import datetime

from database.query_assert_monitor import *


class AssertMonitor:

    def __init__(self, mysql, xn, env):

        self.xn = xn
        self.env = env
        self.mysql = mysql

    def split_time(self, time):
        re = time.split(' ')
        re = re[0].split('-')
        re = re[0] + re[1] + re[2]
        return re

    def count_principal_balance(self, project_no: list, asset_org_no, credit_limit,  quota_type=0, warrant_start_time="1900-01-01 00:00:00"):
        """
        根据项目号计算本金余额
        """
        project_balance = 0

        if quota_type == 0:

            # 当额度类型等于0时为循环
            rpy_principal = 0
            repay_principal = 0
            for projectNo in project_no:
                # 实但放款本金
                id = repay(self.mysql, self.xn, self.env).cbs_loan_amt(projectNo, asset_org_no)['id']
                cbs_loan_amt = repay(self.mysql, self.xn, self.env).cbs_loan_amt(projectNo, asset_org_no)['sum(loan_amt)']

                # 实但还款金额
                cbs_rpy_principal = repay(self.mysql, self.xn, self.env).cbs_rpy_principal(projectNo, asset_org_no)['sum(rpy_principal)']

                # 实但代偿金额
                cbs_repay_principal = repay(self.mysql, self.xn, self.env).cbs_repay_principal(projectNo)['sum(repay_principal)']

                if cbs_loan_amt is not None:

                    if cbs_rpy_principal is None:
                        rpy_principal += 0
                    else:
                        rpy_principal += cbs_rpy_principal
                    if cbs_repay_principal is None:
                        repay_principal += 0
                    else:
                        repay_principal += cbs_repay_principal

                    # 本金余额
                    cbs_principal_balance = cbs_loan_amt - rpy_principal - repay_principal

                    print("循环时，%s 项目计算过后的本金余额为： %s" % (projectNo, cbs_principal_balance, ))
                    project_balance += cbs_principal_balance

                else:
                    # 为通道项目
                    # 通道放款本金
                    p_rpy_principal = 0
                    p_repay_principal = 0
                    pls_loan_amt = repay(self.mysql, self.xn, self.env).pls_loan_principal(projectNo, asset_org_no)['sum(loan_principal)']
                    # 通道还款金额
                    pls_rpy_principal = repay(self.mysql, self.xn, self.env).pls_repay_record_principal(projectNo, asset_org_no)['sum(repay_principal)']
                    # 通道代偿金额
                    pls_repay_principal = repay(self.mysql, self.xn, self.env).pls_compensate_principal(projectNo, asset_org_no)['sum(compensate_principal)']
                    # 本金余额
                    if pls_loan_amt is not None:
                        if pls_rpy_principal is None:
                            p_rpy_principal += 0
                        else:
                            p_rpy_principal += pls_rpy_principal
                        if pls_repay_principal is None:
                            p_repay_principal += 0
                        else:
                            p_repay_principal += pls_repay_principal
                        pls_principal_balance = pls_loan_amt - p_rpy_principal - p_repay_principal
                        print("循环时，%s 项目计算过后的本金余额为： %s" % (projectNo, pls_principal_balance,))
                        project_balance += pls_principal_balance
                    else:
                        print("%s 项目查询实担和通道库都无记录，请检查项目编码是否正确！" % (projectNo,))

        else:
            # 当额度类型等于1时非循环
            for projectNo in project_no:
                cbs_compare_quota = repay(self.mysql, self.xn, self.env).cbs_compare_quota(projectNo, warrant_start_time, asset_org_no)['sum(loan_amt)']
                if cbs_compare_quota is not None:
                    print("非循环时，%s 项目计算过后的本金余额为： %s" % (projectNo, cbs_compare_quota,))
                    project_balance += cbs_compare_quota

                else:
                    # 为通道项目
                    now_time = datetime.datetime.now().__format__('%Y-%m-%d %H:%M:%S')
                    time = self.split_time(now_time)
                    replace_warrant_start_time = self.split_time(warrant_start_time)
                    pls_compare_quota =repay(self.mysql, self.xn, self.env).pls_compare_quota(projectNo, replace_warrant_start_time, time, asset_org_no)['sum(loan_principal)']

                    if pls_compare_quota is not None:
                        print("非循环时，%s 项目计算过后的本金余额为： %s" % (projectNo, pls_compare_quota,))
                        project_balance += pls_compare_quota
                    else:
                        print("%s 项目查询实担和通道库都无记录，请检查项目编码是否正确！" % (projectNo,))

        quota_use_ate = project_balance/credit_limit * 100
        quota_use_ate = round(quota_use_ate, 2)
        print("项目维度额度使用率为：%s%%" % (quota_use_ate, ))

    def count_assert_message(self, assert_no):
        """
        统计资产编号数据结果
        """
        quotaType = {
            "cyclic": "循环",
            "acyclic": "非循环",
            "mix": "混合",
        }
        monitor = {
            "active": "生效中",
            "inactive": "失效"
        }
        prs_assert_message = repay(self.mysql, self.xn, self.env).prs_assert_message(assert_no)
        # 授信额度
        credit_limit = prs_assert_message["quota"]
        # 余额
        balance = prs_assert_message["available_quota"]
        quota_use_ate = balance / credit_limit * 100
        quota_use_ate = round(quota_use_ate, 2)
        # 额度到期日
        expire_end_datetime = prs_assert_message["expire_end_datetime"]
        # 额度类型
        quota_type = prs_assert_message["quota_type"]
        # 监控状态
        monitor_status = prs_assert_message["monitor_status"]
        print("资产编号：%s,监控状态为：%s, 授信额度为：%s, 额度类型为：%s, 额度到期日为：%s, 当前余额为：%s, 额度使用率为：%s%%"
              % (assert_no, monitor.get(monitor_status), credit_limit, quotaType.get(quota_type), expire_end_datetime,
                 balance, quota_use_ate, ))


if __name__ == '__main__':
    # jly是融担环境，mysql=adb，xn=dw时，是查adb库， mysql=rds时，xn=dw时，是查rds库
    mysql = "adb"
    xn = "dw"
    env = "test2"
    # 资产方编号(已页面设置为准)
    assert_no = "360JR"
    # 项目列表，模拟资产编号下的项目(已页面设置为准)
    project = ["5001", "5002", "5003"]
    # 额度类型为0时为循环，为1时为非循环(已页面设置为准)
    quota_type = 0
    # 担保开始时间，可以不传，不传系统默认时间为1900-01-01 00:00:00(已页面设置为准)
    warrant_start_time = "2022-01-01 00:00:00"
    # 授信额度(已页面设置为准)
    credit_limit = 300

    # 资产方统计信息(查rds库)
    # AssertMonitor(mysql, xn, env).count_assert_message(assert_no)

    # 项目统计信息
    AssertMonitor(mysql, xn, env).count_principal_balance(project_no=project, asset_org_no=assert_no,
                                                          credit_limit=credit_limit, quota_type=quota_type,
                                                          warrant_start_time=warrant_start_time)






