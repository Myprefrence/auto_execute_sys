import json
import random
import string
from database.generate_rr import *
from common.scheduler import *


class repay_re:

    def __init__(self, xn, env):
        self.env = env
        self.xn = xn
        self.loanReqNos = []
        self.nowDate = datetime.datetime.now().__format__('%Y-%m-%d %H:%M:%S')

    def repay_no(self):
        ran_int = ''.join(random.sample(string.digits, 8))
        ran_str = ''.join(random.sample(string.ascii_letters, 8))
        repay_n = "repay" + ran_int + ran_str

        return repay_n

    def generate_record(self,order_no,rpyTotalAmt,rpyPrinAmt,rpyIntAmt,rpyOintAmt,rpyOtherAmt,rpyTerm,termSettle="N"):
        url = "https://{}-api{}.jiuliyuntech.com/b2b-front-oms/apiv2/repay/notify".format(self.xn, self.env)
        data = {
            "assetOrgNo": "360JR",
            "assetOrgName": "360金融",
            "fbOrgNo": self.xn,
            "loanReqNo": order_no,
            "sourceCode": "QH",
            "rpyType": "02",
            "rpyTerm": rpyTerm,
            "rpyReqNo": self.repay_no(),
            "payChannel": "ALLINPAY",
            "rpyTotalAmt": rpyTotalAmt,
            "rpyPrinAmt": rpyPrinAmt,
            "rpyIntAmt": rpyIntAmt,
            "rpyOintAmt": rpyOintAmt,
            "rpyOtherAmt": rpyOtherAmt,
            "rpyShareAmt": "0",
            "rpyDeductAmt": "0",
            "rpyRedLineAmt": "0",
            "termSettle": termSettle,
            "rpyOrderNo": "2002",

        }
        headers = {
            "Content-Type": "application/json",
            "isTest": "true"
        }

        response = requests.post(url=url, data=json.dumps(data), headers=headers).json()

        return response


if __name__ == '__main__':
    xn = "xna"
    env = "test1"
    order_no = "t9D0xnAQ1647415947"
    #是否结清 0.本期未结清 1.本期结清
    repay_settle = 1
    #还款类型 01-提前结清 02-按制定期数进行还款
    rpyType = "02"
    #还款期数
    rpyTerm = "1"
    # 还款总金额
    rpyPrinAmt_sum = 600
    #还款本金
    rpyPrinAmt = str(rpyPrinAmt_sum/3)
    #还款利息
    rpyIntAmt = "10"
    #罚息,逾期才可用
    rpyOintAmt = "0"
    #其它费用
    rpyOtherAmt = "0"
    #自定义还款时间
    customize_repay_datetime = ["2022-01-25", "2022-02-25", "2022-03-25", "2022-01-18", "2022-02-18"]
    #自动还款时间
    repay_datetime = datetime.datetime.now().__format__('%Y-%m-%d %H:%M:%S')
    #还款总金额
    rpyTotalAmt = str(float(rpyPrinAmt) + float(rpyIntAmt) + float(rpyOintAmt) + float(rpyOtherAmt))
    cbs_result = generate(xn, env).query_cbs_plan(order_no)
    # print(cbs_result)
    input_command = input("请问您要根据cbs还款计划表进行还款输入0,自定义进行还款请输入1")
    if int(input_command) == 0:
        if len(cbs_result) != 0:
            current_period = 1
            for date in cbs_result:
                schedule_total = date["schedule_total"]
                schedule_principal = date["schedule_principal"]
                schedule_interest = date["schedule_interest"]
                schedule_overdue_fee = date["schedule_overdue_fee"]
                schedule_other_fee = date["schedule_other_fee"]
                response = repay_re(xn, env).generate_record(order_no, str(schedule_total), str(schedule_principal), str(schedule_interest),
                                                  str(schedule_overdue_fee), str(schedule_other_fee), current_period)

                time.sleep(1)
                if response['data']['rpyDesc'] == "还款成功":

                    generate(xn, env).update_cbs_plan(rpy_total_amt=schedule_total, rpy_principal=schedule_principal,
                                                      rpy_interest=schedule_interest,
                                                      rpy_overdue_fee=schedule_overdue_fee,
                                                      rpy_other_fee=schedule_overdue_fee,
                                                      repay_settle=repay_settle,
                                                      last_rpy_datetime=repay_datetime,
                                                      asset_loan_order_no=schedule_other_fee,
                                                      current_period=current_period)
                else:

                    print("还款失败")

                if current_period == int(rpyTerm):
                    break
                else:
                    current_period += 1


        else:
            print("无此订单")

    elif int(input_command) == 1:

        current_period = 1
        for i in range(int(rpyTerm)):
            response = repay_re(xn, env).generate_record(order_no, rpyTotalAmt, rpyPrinAmt, rpyIntAmt, rpyOintAmt,
                                                         rpyOtherAmt, current_period)
            time.sleep(1)
            if response['data']['rpyDesc'] == "还款成功":
                generate(xn, env).update_cbs_plan(rpy_total_amt=rpyTotalAmt, rpy_principal=rpyPrinAmt,
                                                  rpy_interest=rpyIntAmt, rpy_overdue_fee=rpyOintAmt,
                                                  rpy_other_fee=rpyOtherAmt, repay_settle=repay_settle,
                                                  last_rpy_datetime=customize_repay_datetime[i],
                                                  asset_loan_order_no=order_no,
                                                  current_period=current_period,
                                                  )

            else:
                print(response)
                print("还款失败")

            if current_period == int(rpyTerm):
                break
            else:
                current_period += 1

    sh = send_scheduler(env).compensatoryData()
    if sh == "200":
        print("代偿查询执行成功")













