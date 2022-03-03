import json
import random
import string
from common.scheduler import *
from database.queryOffline import *
import datetime


class sendOffline:
    def __init__(self, env):

        self.s = requests.Session()
        self.env = env
        self.task_codes = []
        self.nowDate = datetime.datetime.now().__format__('%Y-%m-%d %H:%M:%S')

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
        # print("登录信息：%s" %(response, ))
        return response["msg"]

    def create_offline_task(self, project_code:str, db_table:str):
        headers = {'Content-Type': 'application/json'}
        url = 'https://oms{}.jiuliyuntech.com/res-oms/task-offline/info/add'.format(self.env)
        data = {
            'projectCode': project_code,
            'type': 'temporary',
            'taskFrequency': '',
            'code': self.loanReqNo(),
            'bizStatus': 'online',
            'name': self.loanReqNo(),
            'params': db_table,
            'taskStartParam': ''
        }
        self.task_codes.append(data["code"])
        print(self.task_codes)
        self.login()
        response = self.s.post(url=url, data=json.dumps(data), headers=headers).json()

        return response

    def main_execute(self, project_code:str, db_table:str):
        print(self.create_offline_task(project_code, db_table))

        for i in range(2):
            time.sleep(2)
            send_scheduler(self.env).offline_execute()

        offline_apply_no = []
        offline_apply_id = []
        count = 0

        for i in self.task_codes:
            offlineTask_result = conn("test1").query_offlineRisk(i)
            for j in offlineTask_result:
                offline_apply_no.append(j["case_no"])
                offline_apply_id.append(j["case_id"])
                print("resOffline结果为: %s\n" % (j,))

                if len(j) != 0:
                    count += 1

        print("offline_apply_no为: %s\n" % (offline_apply_no,))
        print("offline_apply_id为: %s\n" % (offline_apply_id,))
        print("离线跑批案件总数量为: %s" % (count,))


if __name__ == '__main__':
    sendOffline('test2').main_execute("A002", "wangjun")
