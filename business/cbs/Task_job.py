import requests,time,json
from readConfig import *
import urllib3

class testDemo(object):
    # global cookies
    def __init__(self,ur):
        self.ur = ur
        # self.job_num = job_num
        # self.cookies = cookies
    def login(self):
        urllib3.disable_warnings()
        url = 'https://oms%s.jiuliyuntech.com/sso-oms/loginByAjax'%self.ur
        data = "uname=ITADMIN&pwd=itadmin%40jly2021%26&dynamicPwd=&smsCode="
        headers = json.loads(ReadConfig().get_requests('headers1'))
        logn = requests.post(url=url,data=data,headers=headers,verify=False)
        # print(logn.json())
        return logn.cookies
        # globals()['cookies'] = logn.cookies
    def job(self,job_num,cookies):
        time1=time.strftime('%Y-%m-%d')
        data = "jobid=%s&executeTime=%s"%(job_num,time1)
        url = 'https://oms%s.jiuliyuntech.com/scheduler-oms/job/execute'%self.ur
        headers = json.loads(ReadConfig().get_requests('headers1'))
        job = requests.post(url,data,headers=headers,cookies=cookies)
        print(job.json())
    def Huisu(self,id,code,cookie):
        # headers = json.loads(ReadConfig().get_requests('headers1'))
        headers = {
            "accept":"application/json, text/plain, */*",
            "accept-encoding":"gzip, deflate, br",
            "accept-language":"zh-CN,zh;q=0.9",
            "content-length":"139",
            "content-type":"application/json;charset=UTF-8",
            "sec-fetch-dest":"empty",
            "sec-fetch-mode":"cors",
            "sec-fetch-site":"same-origin",
            "user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        }
        url = 'https://oms%s.jiuliyuntech.com/resc-oms/varBackCalc/innerVarBackCalc'%self.ur
        data = {"caseId":id,"caseIdList":[],"projectNoList":[],"startTime":"","endTime":"","interfaceCodeList":[code]}
        Huis = requests.post(url,data=json.dumps(data),headers=headers,cookies=cookie)
        if Huis.status_code == 200:
            print("调用回溯案件接口成功")
        else:
            print("调用回溯案件失败，请检查接口或参数")

if __name__ == '__main__':
        """
        定时推送到cap：cbs_loan_pushcap
        筛选代偿数据：cap_016
        验签初始化：cap_039
        文件验签：cap_040
        """
        ur = "test1"
        job_num = "cbs_job_005"
        id ="XNAA032206160015700236"
        code = "userLoanDetailVar"
        cook = testDemo(ur)
        cookie = cook.login()
        #任务调度
        # cook.job(job_num,ur,cookie)
        #回溯调用
        cook.Huisu(id,code,cookie)