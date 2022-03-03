
import requests
import random
import string
import time
import datetime
import json
from database.querySuspend import *

class suspend_strategy:

    def __init__(self, env, ):

        self.s = requests.Session()
        self.env = env
        self.task_codes = []
        self.startTime = (datetime.datetime.now() + datetime.timedelta(seconds=5)).__format__('%Y-%m-%d %H:%M:%S')
        self.endTime = (datetime.datetime.now() + datetime.timedelta(days=1)).__format__('%Y-%m-%d %H:%M:%S')
        # self.projects = conn().query_project(project)
        # self.strategies = conn().query_strategy(strategy)
        # self.project = self.projects[0]["id"]
        # self.projectId = self.projects[0]["id"]
        # self.projectCode = self.projects[0]["code"]
        # self.projectVersion = self.projects[0]["version"]
        # self.strategy = self.strategies[0]["id"]
        # self.strategyId = self.strategies[0]["id"]
        # self.strategyCode = self.strategies[0]["strategy_code"]
        # self.strategyVersion = self.strategies[0]["version"]

    def loanReqNo(self):
        ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        now_time = str(time.time())
        now_time = now_time.split('.')
        ran_str = ran_str + now_time[0]

        return ran_str

    def login(self):
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "uname": "risk",
            "pwd": "risk@2021&&"
        }
        url = "https://oms{}.jiuliyuntech.com/sso-oms/loginByAjax".format(self.env)
        response = self.s.post(url=url, data=data, headers=headers).json()
        return response["msg"]

    def createSuspend(self, projected, strategy):
        projects = conn(self.env).query_project(projected)

        strategies = conn(self.env).query_strategy(strategy)

        project = projects[0]["id"]
        projectId = projects[0]["id"]
        projectCode = projects[0]["code"]
        projectVersion = projects[0]["version"]
        strategy = strategies[0]["id"]
        strategyId = strategies[0]["id"]
        strategyCode = strategies[0]["strategy_code"]
        strategyVersion = strategies[0]["version"]

        headers = {'Content-Type': 'application/json'}
        data = {
            'project': project,
            'projectId': projectId,
            'projectCode': projectCode,
            'projectVersion': projectVersion,
            'strategy': strategy,
            'strategyId': strategyId,
            'strategyCode': strategyCode,
            'strategyVersion': strategyVersion,
            'startDatetime': self.startTime,
            'expectEndDatetime': self.endTime
        }

        self.login()
        url = "https://oms{}.jiuliyuntech.com/res-oms/suspendManager/createSuspend".format(self.env)
        response = self.s.post(url=url, data=json.dumps(data), headers=headers).json()

        return response

if __name__ == '__main__':
    suspend_result = suspend_strategy("test1").createSuspend("A002", "X009")
    print(suspend_result)
    if suspend_result["message"] == "操作成功":
        print("创建卡件成功")

    else:
        print("创建卡件失败")
    # project_result = conn().query_project('A002')
    # # print(project_result[0]["id"])
    # strategy_result = conn().query_strategy('X008')
    # print(strategy_result)