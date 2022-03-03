import json
import threading
from common.scheduler import *
from common.connectMysql import *
import datetime
from database.generate_rp import *


class send:

    def __init__(self, xn, env):
        self.env = env
        self.xn = xn
        self.loanReqNos = []
        self.nowDate = datetime.datetime.now().__format__('%Y-%m-%d %H:%M:%S')

    #     self.name = random_name()
    #     self.phone = phone_num()
    #     self.ocid = str(CreateIdCardNumber(1).create_id_card_number())

    def loanReqNo(self):
        ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        now_time = str(time.time())
        now_time = now_time.split('.')
        ran_str = ran_str + now_time[0]

        return ran_str

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
            re = str(re[0]) + '-' + str(re[1]) + '-' + re[2]
            list.append(re)

        del list[0]

        return list

    def c_time(self, loan_trem):
        list = []
        now = datetime.datetime.now()
        for i in range(loan_trem + 1):
            re = self.monthdelta(now, i)
            re = re.__format__('%Y-%m-%d %H:%M:%S')
            list.append(re)

        del list[0]

        return list

    def now_time(self):
        re = datetime.datetime.now().__format__('%Y-%m-%d %H:%M:%S')
        re = re.split(' ')
        re = re[0].split('-')
        re = str(re[0]) + '-' + str(re[1]) + '-' + re[2]

        return re

    def re_id(self):
        param = ''.join(str(i) for i in random.sample(string.digits, 8))
        param1 = ''.join(str(i) for i in random.sample(string.digits, 8))
        id = 'XNAC' + param * 2 + param1

        return id

    def cap_no(self):
        param = ''.join(str(i) for i in random.sample(string.digits, 8))
        param1 = ''.join(str(i) for i in random.sample(string.digits, 8))
        cp_n = 'XNAC' + param * 2 + param1

        return cp_n

    def sendorder(self,project:str, id:str, mobile:str,custName:str,loan_term,loanAmt):
        # print(self.phone)
        # print(self.ocid)
        # print(self.loanReqNo())
        headers = {
            "Content-Type": "application/json",
            "isTest": "true"
        }

        url = "https://{}-api{}.jiuliyuntech.com/b2b-front-oms/apiv2/loan/add".format(self.xn, self.env)
        data = {
            "assetOrgNo": "360JR",
            "assetOrgName": "360资产方",
            "fbOrgNo": self.xn,
            "loanReqNo": self.loanReqNo(),
            "sourceCode": "QH",
            "custName": custName,
            "idType": "1",
            "id": id,
            "sex": "F",
            "dbBankCode": "0001",
            "dbAcct": "6217002020039444",
            "dbAcctName": "阳光消金银行",
            "loanDate": self.nowDate,
            "loanAmt": loanAmt,
            "lnTerm": loan_term,
            "rpyType": "03",
            "firstDayDue": "2021-04-03",
            "irrYearRate": "0.075",
            "creditAmt": "18000.00",
            "usedAmt": "0.00",
            "bindCardMobileNo": mobile,
            "mobileNo": mobile,
            "loanPurpose": "08",
            "projectNo": project,
            "creditCardSts": "N",
            "loanAcctSts": "N",
            "creditCardOverdueDays": "N",
            "loanOverdueDays": "N",
            "thirdPartyBlackList": "N",
            "idVerifyRisk": "N",
            "idCert": "Y",
            "ageCheck": "Y",
            "policeInfoNotExist": "N",
            "policeInfoNotMatch": "N",
            "creditTime": self.now_time(),
            "overdueHisMaxDays": "33",
            "overdueHisMaxAmt": "10000.00",
            "custApplyScore": "600",
            "custActScore": "600",
            "agreementNo": "7419476000001",
            "idValidDateStart": "2000-02-02",
            "idValidDateEnd": "2050-02-02",
            "custDegree": "10",
            "contact1Relation": "1",
            "contact1Mobile": "13632700026",
            "monthlyIncome": 10000,
            "contactAddressLocation": "深圳南山",
            "idcardPic": "idcardPicUrl",
            "companyLocation": "深圳后海",
            "ocrIdNation": "汉族",
            "companyName": "公司名称啊",
            "maritalStatus": "10",
            "custOccupation": "2",
            "companyPhoneNo": "18928441605",
            "jobType": "7",
            "ocrIDIssuedBy": "深圳宝安",
            "facePic1": "facePic1Url",
            "facePic2": "facePic2Url",
            "companyAddress": "公司地址啊",
            "ocrIdAddress": "身份证地址啊",
            "contactAddressDetail": "联系地址啊",
            "contact1Name": "黄每夆20211028"
        }

        self.loanReqNos.append(data["loanReqNo"])
        # print(self.loanReqNos)
        response = requests.post(url=url, data=json.dumps(data), headers=headers, verify=False).json()
        print(response)

        if response["message"] == "成功":

            print("发动订单成功")

            # time.sleep(2)
            # send_scheduler(self.env).main_execute()

            for i in range(2):
                send_scheduler(self.env).main_execute()
                time.sleep(3)

        else:

            print("发动订单失败")

    def main(self,thread_number,project, id, mobile, custName, loan_term, loanAmt, rpy_interest=10):

        threadpool = []
        for i in range(thread_number):
            th = threading.Thread(target=self.sendorder, args=(project, id, mobile,custName,loan_term,loanAmt))
            threadpool.append(th)
        for th in threadpool:
            th.start()
            # time.sleep(1)
        for th in threadpool:
            threading.Thread.join(th)

        if len(self.loanReqNos) != 0:
            apply_id = []
            order_no = []
            cap_no = self.cap_no()
            for i in self.loanReqNos:
                # cbs_result = conn().query_orderID(i)
                # rms_result = conn().query_rmsSatus(cbs_result["id"])
                # print("order_no为: %s, order_id为: %s, rms结果为: %s\n" % (i, cbs_result, rms_result))

                res_result = conn(self.xn, self.env).query_res(i)
                # print(res_result)
                if res_result is None:
                    order_no.append(i)
                    pass
                else:
                    apply_id.append(res_result["id"])

                print("order_no为: %s, res结果为: %s\n" % (i, res_result))

                order_result = generate(self.xn, self.env).query_order(i)

                # print(order_result)
                for order in order_result:
                    order_id = order["id"]
                    asset_org_no = order["asset_org_no"]
                    asset_org_name = order["asset_org_name"]
                    cust_no = order["cust_no"]
                    loan_period = order["loan_period"]
                    pro_no = order["project_no"]
                    rpy_principal = round((loanAmt / loan_term), 2)
                    rey_total = rpy_principal + rpy_interest
                    # loan_date = self.r_time(loan_term)
                    loan_date = ["2021-08-17", "2021-09-17", "2021-10-17", "2022-01-18", "2022-02-18"]

                    current_period = 1

                    for j in range(loan_term):
                        generate(self.xn, self.env).repay_plan(self.re_id(), order_id, i, cap_no, loan_term, current_period, loan_date[j], rey_total,
                                                               rpy_principal, rpy_interest, self.nowDate,
                                                               self.nowDate, asset_org_no, asset_org_name, cust_no,
                                                               custName, pro_no, loanAmt)

                        current_period += 1


if __name__ == '__main__':
    loanDate = (datetime.datetime.now() + datetime.timedelta(days=92)).__format__('%Y-%m-%d %H:%M:%S')
    project = "1002"
    custName = "汪离23"
    xn = "xna"
    env = "test1"
    id = "110101199609076995"
    # 110101195508074036
    # 13784559356, 15546457225
    mobile = "15846457224"
    loan_term = 3
    loanAmt = 100
    send(xn, env).main(1, project, id, mobile, custName, loan_term, loanAmt)

    od = ["H6iWlw3M1641784507"]












