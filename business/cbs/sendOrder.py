import json
import threading
from common.name import *
from common.phone import *
from common.ocid import *
from common.scheduler import *
from common.connectMysql import *
import datetime


class send:

    def __init__(self, xn, env):
        self.xn = xn
        self.env = env
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

    def sendorder(self,project):
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
            "custName": random_name(),
            "idType": "1",
            "id": CreateIdCardNumber(1).create_id_card_number()[0],
            "sex": "F",
            "dbBankCode": "0001",
            "dbAcct": "6217002020039444",
            "dbAcctName": "阳光消金银行",
            "loanDate": self.nowDate,
            "loanAmt": "100",
            "lnTerm": "6",
            "rpyType": "03",
            "firstDayDue": "2021-04-03",
            "irrYearRate": "0.075",
            "creditAmt": "18000.00",
            "usedAmt": "0.00",
            "bindCardMobileNo": "13524637079",
            "mobileNo": phone_num(),
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
            "creditTime": "2020-05-01",
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
        # print(response)

        if response["message"] == "成功":

            print("发动订单成功")

            # time.sleep(2)
            # send_scheduler(self.env).main_execute()

            for i in range(2):
                send_scheduler(self.env).main_execute()
                time.sleep(3)

        else:

            print("发动订单失败")

    def main(self, thread_number, project):
        threadpool = []
        for i in range(thread_number):
            th = threading.Thread(target=self.sendorder, args=(project, ))

            threadpool.append(th)

        for th in threadpool:
            th.start()
            # time.sleep(1)
        for th in threadpool:
            threading.Thread.join(th)


        if len(self.loanReqNos) != 0:
            apply_id = []
            order_no = []
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

            if len(apply_id) == 0:
                print("插入res数据异常,未查询到案件数据,order_no为：%s" % (order_no,))

            else:
                print("apply_id数据为: %s" % (apply_id,))


if __name__ == '__main__':
    send("xna", "test2").main(1, "1002")









