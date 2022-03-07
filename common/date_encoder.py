# -*- coding: utf-8 -*-

# @Time : 2022/3/1 18:15

# @Author : WangJun

# @File : date_encoder.py

# @Software: PyCharm


import datetime
import json
import time


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self, obj)


class Date(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return time.mktime(obj.timetuple())
        else:
            return json.JSONEncoder.default(self, obj)

if __name__ == '__main__':
    data = {'id': 'A172203040005100015', 'strategy_code': 'D027', 'strategy_name': 'D027', 'strategy_status': 'online', 'operate_status': 'changing', 'strategy_script': '{"edges":[{"id":"718797b3","index":2,"shape":"flow-polyline","source":"97221000","sourceAnchor":2,"target":"7c00e46f","targetAnchor":0},{"id":"69407b6f","index":3,"shape":"flow-polyline","source":"7c00e46f","sourceAnchor":2,"target":"b5156a54","targetAnchor":0},{"id":"4092b219","index":5,"label":"n>50","shape":"flow-polyline","source":"b5156a54","sourceAnchor":3,"target":"8a7f5ed2","targetAnchor":0},{"id":"10d84e68","index":6,"label":"n<=50","shape":"flow-polyline","source":"b5156a54","sourceAnchor":1,"target":"60c6df7d","targetAnchor":0},{"id":"a4f087d1","index":7,"label":"n>=40","shape":"flow-polyline","source":"60c6df7d","sourceAnchor":3,"target":"cc1a5c6f","targetAnchor":0},{"id":"74763d14","index":8,"label":"n<40","shape":"flow-polyline","source":"60c6df7d","sourceAnchor":1,"target":"bc9f32a9","targetAnchor":0},{"id":"197c359d","index":13,"label":"","shape":"flow-polyline","source":"8a7f5ed2","sourceAnchor":2,"target":"d6634b45","targetAnchor":0},{"id":"49ff9649","index":14,"label":"n>60","shape":"flow-polyline","source":"d6634b45","sourceAnchor":3,"target":"c9579364","targetAnchor":0},{"id":"bb294491","index":15,"label":"n<=60","shape":"flow-polyline","source":"d6634b45","sourceAnchor":1,"target":"3f654bac","targetAnchor":0},{"id":"c1d5b354","index":17,"shape":"flow-polyline","source":"bc9f32a9","sourceAnchor":2,"target":"cff32807","targetAnchor":0},{"id":"71bdec8b","index":20,"label":"n>30","shape":"flow-polyline","source":"cff32807","sourceAnchor":3,"target":"53ef754d","targetAnchor":0},{"id":"9a5eb06e","index":21,"shape":"flow-polyline","source":"3f654bac","sourceAnchor":2,"target":"1b806720","targetAnchor":0},{"id":"e5ecfa49","index":22,"shape":"flow-polyline","source":"c9579364","sourceAnchor":2,"target":"1b806720","targetAnchor":3},{"id":"c55434d8","index":23,"shape":"flow-polyline","source":"53ef754d","sourceAnchor":2,"target":"1b806720","targetAnchor":1},{"id":"1b5b7589","index":24,"shape":"flow-polyline","source":"f97bdfe7","sourceAnchor":2,"target":"1b806720","targetAnchor":1},{"id":"55b64964","index":25,"shape":"flow-polyline","source":"1b806720","sourceAnchor":2,"target":"69b3b9b9","targetAnchor":0},{"id":"7e9c626e","index":26,"shape":"flow-polyline","source":"cc1a5c6f","sourceAnchor":2,"target":"1b806720","targetAnchor":0},{"id":"761a4841","index":30,"label":"n<=30","shape":"flow-polyline","source":"cff32807","sourceAnchor":1,"target":"f97bdfe7","targetAnchor":0}],"nodes":[{"color":"#FA8C16","id":"97221000","index":0,"label":"开始节点","nodetype":"startNode","shape":"flow-circle","size":"72*72","type":"node","x":588.9861145019531,"y":91.33334350585938},{"color":"#1890FF","id":"7c00e46f","index":1,"label":"常规节点","nodetype":"commonNode","size":"100*50","type":"node","x":589.9861145019531,"y":196.66666412353516},{"color":"#13C2C2","id":"60c6df7d","index":4,"label":"条件节点","nodetype":"judgeNode","shape":"flow-rhombus","size":"80*80","type":"node","x":859.9861145019531,"y":415.94444274902344},{"color":"#1890FF","id":"8a7f5ed2","index":9,"label":"常规节点","nodetype":"commonNode","size":"100*50","type":"node","x":339,"y":422},{"color":"#1890FF","id":"cc1a5c6f","index":10,"label":"常规节点","nodetype":"commonNode","size":"100*50","type":"node","x":717,"y":566},{"color":"#1890FF","id":"bc9f32a9","index":11,"label":"常规节点","nodetype":"commonNode","size":"100*50","type":"node","x":1005,"y":566.5},{"color":"#13C2C2","id":"d6634b45","index":12,"label":"条件节点","nodetype":"judgeNode","shape":"flow-rhombus","size":"80*80","type":"node","x":331.9861145019531,"y":566},{"color":"#13C2C2","id":"cff32807","index":16,"label":"条件节点","nodetype":"judgeNode","shape":"flow-rhombus","size":"80*80","type":"node","x":1008.9861145019531,"y":689.4999923706055},{"color":"#1890FF","id":"c9579364","index":18,"label":"常规节点","nodetype":"commonNode","size":"100*50","type":"node","x":155.98611450195312,"y":703.4999923706055},{"color":"#1890FF","id":"53ef754d","index":19,"label":"常规节点","nodetype":"commonNode","size":"100*50","type":"node","x":859.9861145019531,"y":826.0555530115962},{"color":"#1890FF","id":"3f654bac","index":27,"label":"常规节点","nodetype":"commonNode","size":"100*50","type":"node","x":418.9861145019531,"y":689.4999923706055},{"color":"#13C2C2","id":"b5156a54","index":28,"label":"条件节点","nodetype":"judgeNode","shape":"flow-rhombus","size":"80*80","type":"node","x":591.9861145019531,"y":355.5},{"color":"#1890FF","id":"f97bdfe7","index":29,"label":"常规节点","nodetype":"commonNode","size":"100*50","type":"node","x":1149,"y":818},{"color":"#FA8C16","id":"69b3b9b9","index":31,"label":"结束节点","nodetype":"endNode","shape":"flow-circle","size":"80*80","type":"node","x":653,"y":1121},{"color":"#1890FF","id":"1b806720","index":32,"label":"常规节点","nodetype":"commonNode","size":"100*50","type":"node","x":640.4861145019531,"y":998}]}', 'reject_reason': '1', 'remark': '', 'version': '20210825-010', 'online_time': datetime.datetime(2022, 3, 4, 15, 22, 40), 'offline_time': None, 'create_by': '超级管理员', 'create_datetime': datetime.datetime(2021, 8, 25, 14, 15, 48), 'update_by': 'LIANGHUIHUI', 'submit_by': 'LIANGHUIHUI', 'update_datetime': datetime.datetime(2022, 3, 4, 15, 22, 50), 'enable': 'Y'}
    jj = json.dumps(data, cls=Date, ensure_ascii=False)
    print(jj)
