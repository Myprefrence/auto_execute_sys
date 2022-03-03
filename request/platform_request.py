"""
九里云运营平台页面操作部分请求
"""

import request


# 登录九里云运营平台
def login_jly_platform(env: str, data: dict):
    return request.session.post(url=f'https://oms{env}.jiuliyuntech.com/loginByAjax', data=data).json()


# 执行调度任务
def run_schedule_job(env: str, data: dict):
    return request.session.post(url=f'https://oms{env}.jiuliyuntech.com/scheduler-oms/job/execute', data=data).json()


# 执行提交修改中的策略
def submit_strategy(env: str, data: str):
    return request.session.post(
        url=f'https://oms{env}.jiuliyuntech.com/res-oms/strategyInfo/submitStrategyInfoOnEdit',
        data=data, headers={'Content-Type': 'application/json'}).json()


# 执行复核策略-通过
def audit_strategy_pass(env: str, strategy_id: str):
    return request.session.get(url=f'https://oms{env}.jiuliyuntech.com/res-oms/strategyInfo/auditPass?'
                                   f'strategyInfoId={strategy_id}').json()


# 执行复核策略-驳回
def audit_strategy_refuse(env: str, strategy_id: str, refuse_msg: str):
    return request.session.get(url=f'https://oms{env}.jiuliyuntech.com/res-oms/strategyInfo/auditNotPass?'
                                   f'strategyInfoId={strategy_id}&refuseMsg={refuse_msg}').json()


# 执行复核项目-通过
def audit_project_pass(env: str, project_id: str):
    return request.session.get(url=f'https://oms{env}.jiuliyuntech.com/res-oms/projectInfo/auditPass?'
                                   f'projectId={project_id}').json()


# 执行复核项目-驳回
def audit_project_refuse(env: str, project_id: str, refuse_msg: str):
    return request.session.get(url=f'https://oms{env}.jiuliyuntech.com/res-oms/projectInfo/auditNotPass?'
                                   f'projectId={project_id}&msg={refuse_msg}').json()


# 创建离线任务
def create_offline_task(env: str, data: str):
    return request.session.post(f'https://oms{env}.jiuliyuntech.com/res-oms/task-offline/info/add',
                                data=data, headers={'Content-Type': 'application/json'}).json()


# 创建卡件
def create_suspend(env: str, data: str):
    return request.session.post(url=f'https://oms{env}.jiuliyuntech.com/res-oms/suspendManager/createSuspend',
                                data=data, headers={'Content-Type': 'application/json'}).json()


# 下线卡件
def offline_suspend(env: str, data: str):
    return request.session.post(url=f'https://oms{env}.jiuliyuntech.com/res-oms/suspendManager/offline',
                                data=data, headers={'Content-Type': 'application/json'}).json()


# 登录disconf
def login_disconf(data: dict):
    return request.session.post(url='https://disconfdev.jiuliyuntech.com/api/account/signin', data=data).json()


# 获取disconf app列表
def get_app_list():
    return request.session.get(url='https://disconfdev.jiuliyuntech.com/api/app/list').json()


# 获取disconf env列表
def get_env_list():
    return request.session.get(url='https://disconfdev.jiuliyuntech.com/api/env/list').json()


# 获取disconf配置信息
def get_config_list(env_id: str, sys_id: str):
    return request.session.get(url=f'https://disconfdev.jiuliyuntech.com/api/web/config/list?'
                                   f'appId={sys_id}&envId={env_id}&version=1.0.0&').json()


# 编辑disconf指定配置文件配置项
def set_config_item(config_id: str, content: str):
    return request.session.put(url=f'https://disconfdev.jiuliyuntech.com/api/web/config/filetext/{config_id}?'
                                   f'fileContent={content}', headers={'application': 'x-www-form-urlencoded'}).text
