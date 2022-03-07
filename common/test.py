# -*- coding: utf-8 -*-

# @Time : 2022/2/21 15:52

# @Author :Administrator

# @File : HTTP.py

# @Software: PyCharm
# @Desc:http请求：post,get
import datetime

import requests
import json


class requestsUtils:
    def __init__(self):
        self.s = requests.Session()

    def post_main(self, method, url, data, header):
        global res#可以在函数内部对函数外的对象进行操作了
        if method=="post":
            if header =="application/x-www-form-urlencoded":
                res = self.s.post(url=url, data=data)
                print(res.json())
            if header=={"Content-Type": "application/json"}:
                res = self.s .post(url=url, data=json.dumps(data), headers=header)
                print(res)
        # json.dumps()函数用于将 Python 对象编码成 JSON 字符串
        # return json.dumps(res.json(), ensure_ascii=False, sort_keys=True, indent=4)
        # return res.json()

    def get_main(self,method,url, data, header):
        global res
        if method=="get":
            if header != None:
                res = requests.get(url=url, data=data, headers=header)
            else:
                res = requests.get(url=url, data=data)
        return json.dumps(res.json(), ensure_ascii=False, sort_keys=True, indent=4)#转中文为ensure_ascii=False，



if __name__ == '__main__':
    env = "test2"
    s = requests.Session()
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "uname": "risk",
        "pwd": "risk@2021&&"
    }
    url = "https://oms{}.jiuliyuntech.com/sso-oms/loginByAjax".format(env)
    response = s.post(url=url, data=data, headers=headers).json()
    print(response)

    su_url = 'https://omstest2.jiuliyuntech.com/res-oms/strategyInfo/submitStrategyInfoOnEdit'
    su_header = {"Content-Type": "application/json;charset=UTF-8"}
    su_data ={
        "id": "A172109130002410009",
        "strategyCode": "D027",
        "strategyName": "D027",
        "strategyStatus": "online",
        "createDatetime": 1646280011000,
        "enable": "Y",
        "operateStatus": "need_check",
        "rejectReason": "1",
        "updateDatetime": 1646280011000,
        "version": "20210825-010",
        "projectCodeList":[
            "A002",
            "A001"
        ],
       "strategyScript":"{\"nodes\":[{\"color\":\"#FA8C16\",\"id\":\"97221000\",\"index\":0,\"label\":\"开始节点\",\"nodetype\":\"startNode\",\"shape\":\"flow-circle\",\"size\":\"72*72\",\"type\":\"node\",\"x\":588.9861145019531,\"y\":91.33334350585938},{\"color\":\"#1890FF\",\"id\":\"7c00e46f\",\"index\":1,\"label\":\"常规节点\",\"nodetype\":\"commonNode\",\"size\":\"100*50\",\"type\":\"node\",\"x\":589.9861145019531,\"y\":196.66666412353516},{\"color\":\"#13C2C2\",\"id\":\"60c6df7d\",\"index\":4,\"label\":\"条件节点\",\"nodetype\":\"judgeNode\",\"shape\":\"flow-rhombus\",\"size\":\"80*80\",\"type\":\"node\",\"x\":859.9861145019531,\"y\":415.94444274902344},{\"color\":\"#1890FF\",\"id\":\"8a7f5ed2\",\"index\":9,\"label\":\"常规节点\",\"nodetype\":\"commonNode\",\"size\":\"100*50\",\"type\":\"node\",\"x\":339,\"y\":422},{\"color\":\"#1890FF\",\"id\":\"cc1a5c6f\",\"index\":10,\"label\":\"常规节点\",\"nodetype\":\"commonNode\",\"size\":\"100*50\",\"type\":\"node\",\"x\":717,\"y\":566},{\"color\":\"#1890FF\",\"id\":\"bc9f32a9\",\"index\":11,\"label\":\"常规节点\",\"nodetype\":\"commonNode\",\"size\":\"100*50\",\"type\":\"node\",\"x\":1005,\"y\":566.5},{\"color\":\"#13C2C2\",\"id\":\"d6634b45\",\"index\":12,\"label\":\"条件节点\",\"nodetype\":\"judgeNode\",\"shape\":\"flow-rhombus\",\"size\":\"80*80\",\"type\":\"node\",\"x\":331.9861145019531,\"y\":566},{\"color\":\"#13C2C2\",\"id\":\"cff32807\",\"index\":16,\"label\":\"条件节点\",\"nodetype\":\"judgeNode\",\"shape\":\"flow-rhombus\",\"size\":\"80*80\",\"type\":\"node\",\"x\":1008.9861145019531,\"y\":689.4999923706055},{\"color\":\"#1890FF\",\"id\":\"c9579364\",\"index\":18,\"label\":\"常规节点\",\"nodetype\":\"commonNode\",\"size\":\"100*50\",\"type\":\"node\",\"x\":155.98611450195312,\"y\":703.4999923706055},{\"color\":\"#1890FF\",\"id\":\"53ef754d\",\"index\":19,\"label\":\"常规节点\",\"nodetype\":\"commonNode\",\"size\":\"100*50\",\"type\":\"node\",\"x\":859.9861145019531,\"y\":826.0555530115962},{\"color\":\"#1890FF\",\"id\":\"3f654bac\",\"index\":27,\"label\":\"常规节点\",\"nodetype\":\"commonNode\",\"size\":\"100*50\",\"type\":\"node\",\"x\":418.9861145019531,\"y\":689.4999923706055},{\"color\":\"#13C2C2\",\"id\":\"b5156a54\",\"index\":28,\"label\":\"条件节点\",\"nodetype\":\"judgeNode\",\"shape\":\"flow-rhombus\",\"size\":\"80*80\",\"type\":\"node\",\"x\":591.9861145019531,\"y\":355.5},{\"color\":\"#1890FF\",\"id\":\"f97bdfe7\",\"index\":29,\"label\":\"常规节点\",\"nodetype\":\"commonNode\",\"size\":\"100*50\",\"type\":\"node\",\"x\":1149,\"y\":818},{\"color\":\"#FA8C16\",\"id\":\"69b3b9b9\",\"index\":31,\"label\":\"结束节点\",\"nodetype\":\"endNode\",\"shape\":\"flow-circle\",\"size\":\"80*80\",\"type\":\"node\",\"x\":653,\"y\":1121},{\"color\":\"#1890FF\",\"id\":\"1b806720\",\"index\":32,\"label\":\"常规节点\",\"nodetype\":\"commonNode\",\"size\":\"100*50\",\"type\":\"node\",\"x\":640.4861145019531,\"y\":998}],\"edges\":[{\"id\":\"718797b3\",\"index\":2,\"shape\":\"flow-polyline\",\"source\":\"97221000\",\"sourceAnchor\":2,\"target\":\"7c00e46f\",\"targetAnchor\":0},{\"id\":\"69407b6f\",\"index\":3,\"shape\":\"flow-polyline\",\"source\":\"7c00e46f\",\"sourceAnchor\":2,\"target\":\"b5156a54\",\"targetAnchor\":0},{\"id\":\"4092b219\",\"index\":5,\"label\":\"n>50\",\"shape\":\"flow-polyline\",\"source\":\"b5156a54\",\"sourceAnchor\":3,\"target\":\"8a7f5ed2\",\"targetAnchor\":0},{\"id\":\"10d84e68\",\"index\":6,\"label\":\"n<=50\",\"shape\":\"flow-polyline\",\"source\":\"b5156a54\",\"sourceAnchor\":1,\"target\":\"60c6df7d\",\"targetAnchor\":0},{\"id\":\"a4f087d1\",\"index\":7,\"label\":\"n>=40\",\"shape\":\"flow-polyline\",\"source\":\"60c6df7d\",\"sourceAnchor\":3,\"target\":\"cc1a5c6f\",\"targetAnchor\":0},{\"id\":\"74763d14\",\"index\":8,\"label\":\"n<40\",\"shape\":\"flow-polyline\",\"source\":\"60c6df7d\",\"sourceAnchor\":1,\"target\":\"bc9f32a9\",\"targetAnchor\":0},{\"id\":\"197c359d\",\"index\":13,\"label\":\"\",\"shape\":\"flow-polyline\",\"source\":\"8a7f5ed2\",\"sourceAnchor\":2,\"target\":\"d6634b45\",\"targetAnchor\":0},{\"id\":\"49ff9649\",\"index\":14,\"label\":\"n>60\",\"shape\":\"flow-polyline\",\"source\":\"d6634b45\",\"sourceAnchor\":3,\"target\":\"c9579364\",\"targetAnchor\":0},{\"id\":\"bb294491\",\"index\":15,\"label\":\"n<=60\",\"shape\":\"flow-polyline\",\"source\":\"d6634b45\",\"sourceAnchor\":1,\"target\":\"3f654bac\",\"targetAnchor\":0},{\"id\":\"c1d5b354\",\"index\":17,\"shape\":\"flow-polyline\",\"source\":\"bc9f32a9\",\"sourceAnchor\":2,\"target\":\"cff32807\",\"targetAnchor\":0},{\"id\":\"71bdec8b\",\"index\":20,\"label\":\"n>30\",\"shape\":\"flow-polyline\",\"source\":\"cff32807\",\"sourceAnchor\":3,\"target\":\"53ef754d\",\"targetAnchor\":0},{\"id\":\"9a5eb06e\",\"index\":21,\"shape\":\"flow-polyline\",\"source\":\"3f654bac\",\"sourceAnchor\":2,\"target\":\"1b806720\",\"targetAnchor\":0},{\"id\":\"e5ecfa49\",\"index\":22,\"shape\":\"flow-polyline\",\"source\":\"c9579364\",\"sourceAnchor\":2,\"target\":\"1b806720\",\"targetAnchor\":3},{\"id\":\"c55434d8\",\"index\":23,\"shape\":\"flow-polyline\",\"source\":\"53ef754d\",\"sourceAnchor\":2,\"target\":\"1b806720\",\"targetAnchor\":1},{\"id\":\"1b5b7589\",\"index\":24,\"shape\":\"flow-polyline\",\"source\":\"f97bdfe7\",\"sourceAnchor\":2,\"target\":\"1b806720\",\"targetAnchor\":1},{\"id\":\"55b64964\",\"index\":25,\"shape\":\"flow-polyline\",\"source\":\"1b806720\",\"sourceAnchor\":2,\"target\":\"69b3b9b9\",\"targetAnchor\":0},{\"id\":\"7e9c626e\",\"index\":26,\"shape\":\"flow-polyline\",\"source\":\"cc1a5c6f\",\"sourceAnchor\":2,\"target\":\"1b806720\",\"targetAnchor\":0},{\"id\":\"761a4841\",\"index\":30,\"label\":\"n<=30\",\"shape\":\"flow-polyline\",\"source\":\"cff32807\",\"sourceAnchor\":1,\"target\":\"f97bdfe7\",\"targetAnchor\":0}]}",
        "remark": "",
       "outPutVarList":[
           {
               "category": "2",
               "createBy": "LIANGHUIHUI",
               "createDatetime": 1646280011000,
               "dataType": "1",
               "defaultValue": "",
               "enable": "Y",
               "id": "A062203030006300001",
               "objectCode": "D027",
               "objectId": "A172203030005060001",
               "objectType": "strategy_outbound",
               "objectVersion": "20210825-009",
               "optional": "Y",
               "pageNo": 1,
               "pageSize": 10,
               "remark": "",
               "required": "N",
               "updateBy": "LIANGHUIHUI",
               "updateDatetime": 1646280011000,
               "useType": "1",
               "varCode": "credit_query",
               "varName": "待查询三方",
               "uuid": "1646301101288c0376824-fae8-457e-8e3c-1a3b0d966cb8"
           },
           {
               "category": "2",
               "createBy": "LIANGHUIHUI",
               "createDatetime": 1646280011000,
               "dataType": "1",
               "defaultValue": "",
               "enable": "Y",
               "id": "A062203030006300002",
               "objectCode": "D027",
               "objectId": "A172203030005060001",
               "objectType": "strategy_outbound",
               "objectVersion": "20210825-009",
               "optional": "Y",
               "pageNo": 1,
               "pageSize": 10,
               "required": "N",
               "updateBy": "LIANGHUIHUI",
               "updateDatetime": 1646280011000,
               "useType": "1",
               "varCode": "next_credit_step",
               "varName": "下一征信步骤",
               "uuid": "1646301101288999e99cf-2252-4af7-8aeb-7a97e09a019a"
           }
       ],

    }

    # header="application/x-www-form-urlencoded"
   # requestsUtils().post_main(method="post",url=url,data=data,header=header)
   #  res = s.post(url=su_url, data=json.dumps(su_data), headers=su_header)
   #  print(res.text)


# time = "2021-10-17"
# new_time = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
# new_time = datetime.datetime.strftime(new_time,"%Y-%m-%d %H:%M:%S")
now_time = datetime.datetime.now()
new_time = now_time - datetime.timedelta(days=50)
print(new_time)