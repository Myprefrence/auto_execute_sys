
import requests
import time



class send_scheduler:

    def __init__(self, env):
        self.headers = {"Content-Type":"application/x-www-form-urlencoded"}
        self.s = requests.Session()
        self.env = env
        # # 格式: 2021-09-22 10:45:56
        # form_time1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # print(form_time1)

        # 格式: 2021-09-22 10:45:56
        self.form_time2 = time.strftime("%Y-%m-%d", time.localtime())
        # print(self.form_time2)
        #
        # # 格式：20210922104556
        # form_time3 = time.strftime("%Y%m%d%H%M%S", time.localtime())
        # print(form_time3)

    def login(self):
        data = {
            "uname":"risk",
            "pwd":"risk@2021&&"
        }
        url = "https://oms{}.jiuliyuntech.com/sso-oms/loginByAjax".format(self.env)
        response = self.s.post(url=url, data=data, headers=self.headers).json()
        return response["msg"]

    def initOrder(self):


        data = {
            "jobid": "cbs_loan_initorder",
            "executeTime": self.form_time2
        }
        url = "https://oms{}.jiuliyuntech.com/scheduler-oms/job/execute".format(self.env)
        response = self.s.post(url=url, data=data, headers=self.headers).json()

        return response["code"]

    def credit(self):
        data = {
            "jobid": "cbs_loan_credit",
            "executeTime": self.form_time2
        }
        url = "https://oms{}.jiuliyuntech.com/scheduler-oms/job/execute".format(self.env)
        response = self.s.post(url=url, data=data, headers=self.headers).json()

        return response["code"]

    def automatic_risk(self):
        data = {
            "jobid": "cbs_loan_credit",
            "executeTime": self.form_time2
        }
        url = "https://oms{}.jiuliyuntech.com/scheduler-oms/job/execute".format(self.env)
        response = self.s.post(url=url, data=data, headers=self.headers).json()

        return response["code"]

    def offline_risk(self):
        data = {
            "jobid": "res_001",
            "executeTime": self.form_time2
        }
        url = "https://oms{}.jiuliyuntech.com/scheduler-oms/job/execute".format(self.env)
        response = self.s.post(url=url, data=data, headers=self.headers).json()

        return response["code"]

    def creditStatusTask(self):
        data = {
            "jobid": "cap_009",
            "executeTime": self.form_time2
        }
        url = "https://oms{}.jiuliyuntech.com/scheduler-oms/job/execute".format(self.env)
        response = self.s.post(url=url, data=data, headers=self.headers).json()

        return response["code"]

    def loanStatusTask(self):
        data = {
            "jobid": "cap_010",
            "executeTime": self.form_time2
        }
        url = "https://oms{}.jiuliyuntech.com/scheduler-oms/job/execute".format(self.env)

        response = self.s.post(url=url, data=data, headers=self.headers).json()

        return response["code"]

    def offline_execute(self):
        login_result = self.login()
        if "登录成功" in login_result:
            print("Y")
            offline = self.offline_risk()
            print(offline)
            if offline == "200":
                print("初始化离线任务成功")
        else:
            print("N")

    def compensatoryData(self):
        self.login()
        data = {
            "jobid": "cap_016",
            "executeTime": ""
        }
        url = "https://oms{}.jiuliyuntech.com/scheduler-oms/job/execute".format(self.env)

        response = self.s.post(url=url, data=data, headers=self.headers).json()

        return response["code"]

    def main_execute(self):
        login_result = self.login()
        if "登录成功" in login_result:
            print("Y")
            initOrder_result = self.initOrder()
            if initOrder_result == "200":
                print("初始化成功")
                credit_result = self.credit()
                if credit_result == "200":
                    print("授信成功")
                    automatic_result = self.automatic_risk()
                    if automatic_result == "200":
                        print("自动风控成功")
                        time.sleep(0.5)
                        loanStatus_result = self.loanStatusTask()
                        if loanStatus_result == "200":
                            print("借款状态查询成功")
                            time.sleep(0.5)
                            creditStatus = self.creditStatusTask()
                            if creditStatus == "200":
                                print("授信状态查询成功")

        else:
            print("N")

if __name__ == '__main__':
    send_scheduler("test1").compensatoryData()