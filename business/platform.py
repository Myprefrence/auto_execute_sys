import datetime
import json
import os
import time
import uuid
from urllib import parse

import paramiko

from business import logger
from common import normal
from database.res import jly_query
from request import platform_request


class JlyPlatform:
    """
    @desc
    九里云运营平台页面操作部分

    :param environment  测试环境 (test1, test2), 为空则读取配置文件
    :param virtual      融担环境 (xna, xnb), 为空则读取配置文件
    :param username     登陆用户, 为空则读取配置文件
    :param password     登录密码, 为空则读取配置文件
    :param login        初始化时是否进入登录状态, 默认不进行登录

    @func do_login                  登录九里云运营平台
    @func do_run_schedule_job       执行调度任务
    @func do_submit_strategy        提交策略
    @func do_audit_strategy         复核策略 (包含提交策略步骤)
    @func do_audit_project          复核项目
    @func do_create_offline_task    创建离线任务
    @func do_create_suspend         创建卡件
    @func do_offline_suspend        下线卡件
    """

    def __init__(self, environment=None, virtual=None, username=None, password=None, login=False):
        config = normal.get_config(r'config\platform_config.ini')
        self.root_path = normal.get_root_path()

        self.environment = config.get('environment', 'env') if environment is None else environment
        self.virtual = config.get('environment', 'vir') if virtual is None else virtual
        self.username = config.get(f'jly_{self.environment}', 'itadmin_username') if username is None else username
        self.password = config.get(f'jly_{self.environment}', 'itadmin_password') if password is None else password

        if login:
            self.do_login()

    def do_login(self, username=None, password=None):
        # 登录九里云运营平台

        username = self.username if username is None else username
        password = self.password if password is None else password

        data = {
            'uname': username,
            'pwd': password,
            'dynamicPwd': '',
            'smsCode': ''
        }
        logger.info(f'登录请求参数: {data}')

        response = platform_request.login_jly_platform(env=self.environment, data=data)
        logger.info(f'登录请求响应: {response}')

    def do_run_schedule_job(self, job_list: list):
        # 执行调度任务
        # job_list 待执行任务列表, 在params\jly_platform.json中可配置调度任务字典

        platform_data = json.load(open(rf'{self.root_path}\params\platform_data.json', encoding='utf-8'))
        schedule_job = platform_data['schedule_job']

        for job_no in job_list:
            data = {
                'jobid': schedule_job[str(job_no)],
                'executeTime': datetime.datetime.now().__format__('%Y-%m-%d')
            }
            logger.info(f'执行调度任务请求参数: {data}')

            response = platform_request.run_schedule_job(env=self.environment, data=data)
            logger.info(f'执行调度任务请求响应: {response}')

    def do_submit_strategy(self, strategy_code: str, strategy_info=None):
        # 执行提交策略

        if strategy_info is None:
            strategy_info = jly_query.get_strategy_info_by_code(self.environment, strategy_code)

            operate_status = strategy_info['operate_status']
            if not operate_status == 'changing':
                logger.error(f'当前策略状态: operate_status={operate_status}, 禁止操作')
                return

            logger.info(f'当前策略状态: operate_status={operate_status}')

            # 获取策略关联支持的项目
            project_ref_into_list = jly_query.get_strategy_ref_project(self.environment, strategy_code)

            project_ref_code_list = []
            for project_info in project_ref_into_list:
                project_ref_code_list.append(project_info['project_code'])

            # 更新策略版本, 未上线的项目没有版本, 需要插入版本记录
            version = strategy_info['version']
            if version is not None:
                new_version = int(version[9:]) + 1
                new_version_str = f'00{new_version}' if new_version < 10 \
                    else f'0{new_version}' if new_version < 100 else new_version
                version = f'{version[: 8]}-{new_version_str}'
            else:
                version = datetime.datetime.now().__format__('%Y%m%d%H%M%S')[: 9]

            # 获取策略输出变量
            strategy_output_variable_list = jly_query.get_strategy_output_variable(
                self.environment, strategy_code, version)

            output_variable_list = []
            for strategy_output_variable in strategy_output_variable_list:
                output_variable_list.append({
                    'category': strategy_output_variable['category'],
                    'createBy': 'risk',
                    'createDatetime': normal.get_timestamp(strategy_output_variable['create_datetime'],
                                                           size=10),
                    'dataType': strategy_output_variable['data_type'],
                    'defaultValue': strategy_output_variable['default_value'],
                    'enable': strategy_output_variable['enable'],
                    'id': strategy_output_variable['id'],
                    'objectCode': strategy_output_variable['object_code'],
                    'objectId': strategy_output_variable['object_id'],
                    'objectType': strategy_output_variable['object_type'],
                    'objectVersion': strategy_info['version'],
                    'optional': strategy_output_variable['optional'],
                    'pageNo': 1,
                    'pageSize': 10,
                    'remark': strategy_output_variable['remark'],
                    'required': strategy_output_variable['required'],
                    'updateBy': 'risk',
                    'updateDatetime': normal.get_timestamp(strategy_output_variable['update_datetime']),
                    'useType': strategy_output_variable['use_type'],
                    'varCode': strategy_output_variable['var_code'],
                    'varName': strategy_output_variable['var_name'],
                    'uuid': str(uuid.uuid1())
                })

            # 整合上面所有需要的数据, 发起提交策略请求
            request_data = {
                'id': strategy_info['id'],
                'strategyCode': strategy_code,
                'strategyName': strategy_info['strategy_name'],
                'projectCodeList': project_ref_code_list,
                'strategyStatus': 'online',
                'remark': '',
                'strategyScript': strategy_info['strategy_script'],
                'outPutVarList': output_variable_list,
                'createBy': 'risk',
                'createDatetime': normal.get_timestamp(strategy_info['create_datetime']),
                'enable': strategy_info['enable'],
                'operateStatus': 'need_check',
                'pageNo': 1,
                'pageSize': 10,
                'updateBy': 'risk',
                'updateDatetime': normal.get_timestamp(datetime.datetime.now().__format__('%Y-%m-%d %H:%M:%S')),
                'version': strategy_info['version']
            }

            online_time = strategy_info['online_time']
            if online_time is not None:
                request_data['onlineTime'] = normal.get_timestamp(online_time)

            json_data = json.dumps(request_data)
            logger.info(f'提交策略请求参数: {json_data}')
            response = platform_request.submit_strategy(env=self.environment, data=json_data)
            logger.info(f'提交策略请求响应: {response}')

    def do_audit_strategy(self, strategy_code: str, audit_result='Y', refuse_msg='null'):
        # 提交&复核策略
        # 策略状态为修改中(changing)/待复核(need_check)/待上线(wait_online)时才可执行
        # audit_result 复核结果, Y(默认)-通过 N-驳回
        # refuse_msg 驳回原因, 选填

        audit_result = audit_result.upper()
        if audit_result not in ('Y', 'N'):
            logger.error(f'复核结果不正确: {audit_result}')
            return

        logger.info(f'查询策略信息: strategy_code={strategy_code}')
        strategy_info = jly_query.get_strategy_info_by_code(self.environment, strategy_code)

        if strategy_info is None:
            logger.error(f'策略记录不存在!')
        else:
            response = None
            logger.info(f'策略查询结果: strategy_info={strategy_info}')

            strategy_id = strategy_info['id']
            operate_status = strategy_info['operate_status']

            if operate_status not in ('changing', 'need_check', 'waite_online'):
                logger.error(f'当前策略状态: operate_status={operate_status}, 禁止操作')
            else:
                logger.info(f'当前策略状态: operate_status={operate_status}')

            if operate_status in ('changing', 'need_check', 'waite_online'):
                # 如果策略状态是修改中, 先执行提交
                if operate_status == 'changing':
                    self.do_submit_strategy(strategy_code, strategy_info=strategy_info)

                # 修改最新归档记录的提交者字段, 复核时不会再检测到提交者和复核者一致而无法复核
                latest_archive = jly_query.get_strategy_latest_archive_info(self.environment, strategy_code)
                archive_id = latest_archive['id']

                jly_query.update_strategy_submitter(self.environment, archive_id)
                logger.info(f'修改策略最新归档信息: archive_id={archive_id} 的提交者记录')

                if audit_result == 'Y':
                    logger.info(f'执行复核策略通过请求: strategy_id={strategy_id}')
                    response = platform_request.audit_strategy_pass(self.environment, strategy_id)

                if audit_result == 'N':
                    logger.info(f'执行复核策略驳回请求: strategy_id={strategy_id}, refuse_msg={refuse_msg}')
                    response = platform_request.audit_strategy_refuse(self.environment, strategy_id, refuse_msg)

                logger.info(f'执行复核策略响应: {response}')

    def do_audit_project(self, project_code: str, audit_result='Y', refuse_msg='null'):
        # audit_result 复核结果, Y(默认)-通过 N-驳回

        audit_result = audit_result.upper()
        if audit_result not in ('Y', 'N'):
            logger.error(f'复核结果不正确: {audit_result}')
            return

        logger.info(f'查询项目信息: project_code={project_code}')
        project_info = jly_query.get_project_info_by_code(self.environment, project_code)

        if project_info is None:
            logger.error(f'项目记录不存在!')
        else:
            project_id = project_info['id']
            operate_status = project_info['op_status']

            if operate_status not in ('need_check', 'waite_online'):
                logger.error(f'当前项目状态: operate_status={operate_status}, 禁止操作')
            else:
                response = None
                logger.info(f'当前策略状态: operate_status={operate_status}')

                latest_archive = jly_query.get_project_latest_archive_info(self.environment, project_code)
                archive_id = latest_archive['id']

                jly_query.update_project_submitter(self.environment, archive_id)
                logger.info(f'修改项目最新归档信息: archive_id={archive_id} 的提交者记录')

                if audit_result == 'Y':
                    logger.info(f'执行复核项目通过请求: project_id={project_id}')
                    response = platform_request.audit_project_pass(self.environment, project_id)

                if audit_result == 'N':
                    logger.info(f'执行复核项目驳回请求: project_id={project_id}, refuse_msg={refuse_msg}')
                    response = platform_request.audit_project_refuse(self.environment, project_id, refuse_msg)

                logger.info(f'执行复核项目响应: {response}')

    def do_create_offline_task(self, task_table: str, project_code: str, task_name=None):
        # 创建离线任务
        # task_table 离线任务关联的离线表
        # project_code 离线任务关联的风控项目编号
        # task_code 离线任务的名称, 选填

        if task_name is None:
            task_name = f'task{normal.get_timestamp(datetime.datetime.now(), size=10)}'

        data = json.dumps({
            'projectCode': project_code,
            'type': 'temporary',
            'taskFrequency': '',
            'code': task_name,
            'bizStatus': 'online',
            'name': task_name,
            'params': task_table,
            'taskStartParam': ''
        })
        logger.info(f'创建离线任务请求参数: {data}')

        response = platform_request.create_offline_task(self.environment, data)
        logger.info(f'创建离线任务请求响应: {response}')

    def do_create_suspend(self, project_code: str, strategy_code: str, valid_time=30, invalid_time=3600):
        # 创建卡件
        # project_code: 目标风控项目编号
        # strategy_code: 目标策略编号
        # valid_time: 卡件距离当前时间多久之后生效, 单位-秒
        # invalid_time: 卡件距离当前时间多久之后失效, 单位-秒

        logger.info(f'查询项目&策略信息: project_code={project_code}, strategy_code={strategy_code}')
        project_info = jly_query.get_project_info_by_code(self.environment, project_code)
        strategy_info = jly_query.get_strategy_info_by_code(self.environment, strategy_code)

        if project_info is None:
            logger.error('项目记录不存在!')
        elif strategy_info is None:
            logger.error('策略记录不存在!')
        else:
            now_time = datetime.datetime.now()

            data = json.dumps({
                'project': project_info['id'],
                'projectId': project_info['id'],
                'projectCode': project_code,
                'projectVersion': project_info['version'],
                'strategy': strategy_info['id'],
                'strategyId': strategy_info['id'],
                'strategyCode': strategy_code,
                'strategyVersion': strategy_info['version'],
                'startDatetime': normal.get_datetime(now_time, seconds_diff=valid_time, return_str=True),
                'expectEndDatetime': normal.get_datetime(now_time, seconds_diff=invalid_time, return_str=True)
            })
            logger.info(f'提交创建卡件请求参数: {data}')

            response = platform_request.create_suspend(self.environment, data)
            logger.info(f'提交创建卡件请求响应: {response}')

    def do_offline_suspend(self, project_code: str):
        # 下线最近一条有效卡件记录

        logger.info(f'查询最近有效卡件项目记录: project_code={project_code}')
        suspend_info = jly_query.get_valid_suspend_info(self.environment, project_code)

        if suspend_info is None:
            logger.error(f'未查询到最近有效卡件项目记录')
        else:
            data = json.dumps({
                'bizStatus': suspend_info['biz_status'],
                'createBy': suspend_info['create_by'],
                'enable': suspend_info['enable'],
                'expectEndDatetime': normal.get_timestamp(suspend_info['expect_end_datetime']),
                'id': suspend_info['id'],
                'projectCode': project_code,
                'projectId': suspend_info['project_id'],
                'projectVersion': suspend_info['project_version'],
                'startDatetime': normal.get_timestamp(suspend_info['start_datetime']),
                'strategyCode': suspend_info['strategy_code'],
                'strategyId': suspend_info['strategy_id'],
                'strategyVersion': suspend_info['strategy_version'],
                'suspendType': suspend_info['suspend_type'],
                'updateDatetime': normal.get_timestamp(datetime.datetime.now())
            })
            logger.info(f'下线卡件请求参数: {data}')

            response = platform_request.offline_suspend(self.environment, data)
            logger.info(f'下线卡件请求响应: {response}')


class Disconf:
    """
    @desc
    Disconf 操作

    :param username     登录用户
    :param password     登录密码
    :param login        新建实例对象时是否为登录状态

    @func do_login                      登录 Disconf
    @func do_get_config_list            获取指定系统配置文件列表
    @func do_get_config_id              获取指定系统配置文件 ID
    @func do_get_item_content           获取指定系统配置文件的内容
    @func do_get_item_dict              获取指定系统配置文件的内容, 以字典类型返回
    @func do_set_config_item            新增或修改指定系统配置文件的配置项
    @func do_explanatory_config_item    注释指定系统配置文件的配置项
    @func do_remove_config_item         删除指定系统配置文件的配置项
    """

    def __init__(self, username=None, password=None, login=False):
        config = normal.get_config(r'config\platform_config.ini')

        self.username = config.get('disconf', 'username') if username is None else username
        self.password = config.get('disconf', 'password') if password is None else password

        self.app_list = None
        self.env_list = None

        if login:
            self.do_login(self.username, self.password)

    def do_login(self, username=None, password=None):
        # 登录Disconf

        username = self.username if username is None else username
        password = self.password if password is None else password

        data = {
            'name': username,
            'password': password,
            'remember': '1'
        }

        logger.info(f'登录请求参数: {data}')
        response = platform_request.login_disconf(data)
        logger.info(f'登录请求响应: {response}')

        self.app_list = self.get_app_list()
        self.env_list = self.get_env_list()

    @staticmethod
    def get_app_list():
        # 获取disconf app列表

        app_list = []
        response = platform_request.get_app_list()

        try:
            app_list = response['page']['result']
        except IndexError:
            logger.error(f'获取disconf app列表返回结果有误: {response}')
        else:
            logger.info(f'获取disconf app列表返回结果: app_list={app_list}')

        return app_list

    @staticmethod
    def get_env_list():
        # 获取disconf env列表

        env_list = []
        response = platform_request.get_env_list()

        try:
            env_list = response['page']['result']
        except IndexError:
            logger.error(f'获取disconf env列表返回结果有误: {response}')
        else:
            logger.info(f'获取disconf env列表返回结果: env_list={env_list}')

        return env_list

    def do_get_config_list(self, env_name: str, app_name: str):
        # 获取指定系统配置文件列表
        # env_name: 测试环境
        # app_name: 系统名称, 如fb-cbs-oms, jly-res-core

        config_list = []
        if len(self.env_list) > 0 and len(self.app_list) > 0:

            env_id = None
            app_id = None
            logger.info(f'获取系统配置文件列表入参: env_name={env_name}, app_name={app_name}')

            for env in self.env_list:
                if env['name'] == env_name:
                    env_id = env['id']
                    break

            for app in self.app_list:
                if app['name'] == app_name:
                    app_id = app['id']
                    break

            if env_id is None:
                logger.error(f'未查询到env_id')
            elif app_id is None:
                logger.error(f'未查询到app_id')
            else:
                logger.info(f'获取系统配置文件列表请求参数: env_id={env_id}, app_id={app_id}')
                response = platform_request.get_config_list(env_id, app_id)

                try:
                    config_list = response['page']['result']
                except IndexError:
                    logger.error(f'获取系统配置文件列表响应结果有误: {response}')
                else:
                    logger.info(f'获取系统配置文件列表响应结果: {config_list}')

        return config_list

    def do_get_config_id(self, env_name: str, app_name: str, filename: str):
        # 获取指定系统配置文件ID

        logger.info(f'获取系统配置文件ID入参: filename={filename}')
        config_list = self.do_get_config_list(env_name, app_name)

        if len(config_list) > 0:
            for config in config_list:
                if config['key'] == filename:
                    config_id = config['configId']
                    logger.info(f'获取系统配置文件ID结果: config_id={config_id}')
                    return config_id

        logger.error(f'未查询到系统配置文件ID！')

    def do_get_item_content(self, env_name: str, app_name: str, filename: str):
        # 获取系统配置文件内容, 返回文本
        # filename: 配置文件名称

        logger.info(f'获取系统配置文件内容入参: filename={filename}')
        config_list = self.do_get_config_list(env_name, app_name)

        if len(config_list) > 0:
            for config in config_list:
                if filename == config['key']:
                    content = config['value']
                    logger.info(f'获取系统配置文件内容结果: \n{content}')
                    return content

            logger.error(f'未查询到系统配置文件: filename={filename}')

    def do_get_item_dict(self, env_name: str, app_name: str, filename: str):
        # 获取系统配置文件内容, 返回字典类型

        config_dict = {}
        content = self.do_get_item_content(env_name, app_name, filename)
        content_list = content.split('\n')

        if len(content_list) == 0:
            logger.error(f'系统配置文件内容不规范: content={content}')

        else:
            for item in content_list:
                if not len(item) == 0 and not item[0] == '#':
                    try:
                        key = item.split('=')[0]
                        value = item[item.find('=') + 1:]
                    except IndexError:
                        logger.error(f'系统配置文件配置项不规范: item={item}')
                        config_dict.clear()
                        break
                    else:
                        config_dict[key] = value

        logger.info(f'获取系统配置文件内容字典: {config_dict}')
        return config_dict

    @staticmethod
    def set_content(key: str, content_list: list, action: str, value=None):
        found_item = False
        new_content = ''

        for content_item in content_list:
            if key in content_item:
                item_key = content_item.split('=')[0]

                if not content_item[0] in ('#', ' ', '\n') and key == item_key:
                    found_item = True

                    if action == 'set':
                        content_item = f'{key}={value}'
                    if action == 'explanatory':
                        print('ok')
                        content_item = f'# {content_item}'

                if action == 'remove':
                    item_key = item_key.replace(' ', '')
                    if key == item_key or f'#{key}' == item_key:
                        continue

            new_content += f'{content_item}\n'

        if not found_item and action == 'set':
            new_content += f'{key}={value}\n'

        return new_content[: -1]

    def do_set_config_item(self, env_name: str, app_name: str, filename: str, item_key=None, item_value=None,
                           items=None):
        """
        新增或修改指定系统配置文件的配置项
        指定配置项不存在则新增, 存在则修改

        item_key        配置项键
        item_value      配置项值
        items           可批量新增或修改, 入参格式:
                        {item_1_key: item_2_value, item_2_key: item_2_value, ...}
        """

        logger.info(f'编辑文件配置项入参: item_key={item_key}, item_value={item_value}')
        content = self.do_get_item_content(env_name, app_name, filename)

        if item_key is not None and item_value is not None:
            logger.info(f'编辑文件配置项入参数据: item_key={item_key}, item_value={item_value}')
            content = self.set_content(key=item_key, value=item_value, content_list=content.split('\n'), action='set')

        if items is not None:
            if isinstance(items, dict):
                for item_key in items:
                    item_value = items[item_key]
                    content = self.set_content(
                        key=item_key, value=item_value, content_list=content.split('\n'), action='set')
            else:
                logger.error(f'批量编辑文件配置项入参数据有误: items={items}')

        config_id = self.do_get_config_id(env_name, app_name, filename)
        content = parse.quote(content)

        logger.info(f'编辑文件配置项请求参数: config_id={config_id}, content={content}')
        response = platform_request.set_config_item(config_id, content)
        logger.info(f'编辑文件配置项响应结果: {response}')

    def do_operate_item(self, env_name: str, app_name: str, filename: str, items: all, action: str):
        # 执行系统配置文件配置项的注释或删除操作

        action_log_str = '注释' if action == 'explanatory' else '删除' if action == 'remove' else None

        logger.info(f'{action_log_str}文件配置项入参: items={items}')
        content = self.do_get_item_content(env_name, app_name, filename)

        if items is not None:

            if type(items) in (str, int, float):
                items = str(items)
                content = self.set_content(key=items, content_list=content.split('\n'), action=action)
            elif type(items) in (list, dict, set, tuple):
                for item in items:
                    content = self.set_content(key=item, content_list=content.split('\n'), action=action)
            else:
                logger.error(f'{action_log_str}文件配置项入参数据有误: items={items}')
                return None

            config_id = self.do_get_config_id(env_name, app_name, filename)
            content = parse.quote(content)

            logger.info(f'{action_log_str}文件配置项请求参数: ')
            response = platform_request.set_config_item(config_id, content)
            logger.info(f'{action_log_str}文件配置项响应结果: {response}')

        else:
            logger.error(f'配置项不能为空!')

    def do_explanatory_config_item(self, env_name: str, app_name: str, filename: str, items: all):
        # 注释系统配置文件的配置项, 可批量操作
        # 指定配置项存在则注释, 不存在则不操作

        self.do_operate_item(env_name, app_name, filename, items, action='explanatory')

    def do_remove_config_item(self, env_name: str, app_name: str, filename: str, items: all):
        # 删除系统配置文件的配置项, 可批量删除
        # 指定配置项存在则删除, 不存在则不操作

        self.do_operate_item(env_name, app_name, filename, items, action='remove')


class SSHConnect:
    """
    @desc
    Linux Shell指令操作, 单个方法可能包含多个命令的执行

    :param env      建立 SSH 连接的服务器名称, 在 config/ssh.ini 下配置或手动输入
    :param hostname 建立 SSH 连接的服务器 IP
    :param port     建立 SSH 连接的服务器端口
    :param username 建立 SSH 连接的用户
    :param password 建立 SSH 连接的密码
    :param connect  建立 SSH 连接时是否为登录状态

    @func connect                   建立 SSH 连接后执行登录
    @func get_all_system            获取 /app 下的所有系统目录名称, 返回列表
    @func get_system_core_root_path 获取指定系统的后端根目录
    @func get_system_oms_root_path  获取指定系统的前端根目录
    @func upload_file               通过 SFTP 上传指定文件到指定目录
    """

    def __init__(self, env=None, hostname=None, port=None, username=None, password=None, connect=False):
        config = normal.get_config(r'config\ssh.ini')
        self.config_env = config.sections()

        self.env = env
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password

        if self.env is not None:
            if self.env not in self.config_env:
                logger.error(f'不存在的环境配置信息: {self.env}')
            else:
                self.hostname = config.get(self.env, 'hostname') if hostname is None else hostname
                self.port = config.get(self.env, 'port') if port is None else port
                self.username = config.get(self.env, 'username') if username is None else username
                self.password = config.get(self.env, 'password') if password is None else password

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        if connect:
            self.connect(self.hostname, self.port, self.username, self.password)

    def connect(self, hostname=None, port=None, username=None, password=None):
        hostname = self.hostname if hostname is None else hostname
        port = self.port if port is None else port
        username = self.username if username is None else username
        password = self.password if password is None else password

        logger.info(f'登录数据: hostname={hostname}, port={port}, username={username}, password={password}')
        self.ssh.connect(hostname=hostname, port=port, username=username, password=password, allow_agent=False)

        self.hostname = hostname if not hostname == self.hostname else self.hostname
        self.port = port if not port == self.port else self.port
        self.username = username if not username == self.username else self.username
        self.password = password if not password == self.password else self.password

    def get_all_system(self):
        std_in, std_out, std_err = self.ssh.exec_command('ls /app')
        system_list = std_out.read().decode('utf-8').split('\n')
        system_list.remove('')
        return system_list

    @staticmethod
    def get_std_out(std_out: object, std_err: object):
        std_out = (std_out.read().decode('utf-8'))[: -1]
        if len(std_out) == 0:
            return (std_err.read().decode('utf-8').remove('\n'))[: -1]
        else:
            return std_out

    def get_system_path(self, system: str, target: str):
        system_name = system.split('-')[1]
        std_in, std_out, std_err = '', '', ''

        if system in self.get_all_system():

            if target == 'core':
                std_in, std_out, std_err = self.ssh.exec_command(
                    f'cd /app/{system}/jetty/{system_name}-core; pwd')
            if target == 'oms':
                std_in, std_out, std_err = self.ssh.exec_command(
                    f'cd /app/{system}/tomcat/webapps/{system_name}-oms; pwd')

            return self.get_std_out(std_out, std_err)

    def get_system_core_root_path(self, system: str):
        std_out = self.get_system_path(system=system, target='core')
        logger.info(f'获取 {system} 系统后端根目录路径结果: {std_out}')
        return std_out

    def get_system_oms_root_path(self, system: str):
        std_out = self.get_system_path(system=system, target='oms')
        logger.info(f'获取 {system} 系统前端根目录路径结果: {std_out}')
        return std_out

    def upload_file(self, local_file: str, remote_path: str,
                    create_dir_if_not_exists=False, override_file_if_exists=False):
        """
        local_file                  本地文件绝对路径
        remote_path                 目标目录绝对路径
        create_dir_if_not_exists    目标目录不存在时, 是否批量创建目录
        override_file_if_exists     目标文件存在时, 是否覆盖文件
        """

        if not os.path.exists(local_file):
            logger.error(f'本地文件不存在: {local_file}')
        else:
            sftp = self.ssh.open_sftp()
            logger.info(f'上传本地文件: {local_file} 到目标路径: {remote_path}')
            linux_file = f'{remote_path}/{os.path.split(local_file)[1]}'

            try:
                sftp.chdir(remote_path)
            except FileNotFoundError:
                if create_dir_if_not_exists:
                    self.ssh.exec_command(f'mkdir -p {remote_path}')
                    logger.info(f'目标目录不存在, 批量创建目录: {remote_path}')
                    time.sleep(1)
                    sftp.put(local_file, linux_file)
                    logger.info('上传成功')
                else:
                    logger.error(f'目标目录不存在: {remote_path}')
            else:
                try:
                    sftp.stat(linux_file)
                except FileNotFoundError:
                    sftp.put(local_file, linux_file)
                    logger.info('上传成功')
                else:
                    if override_file_if_exists:
                        sftp.put(local_file, linux_file)
                        logger.info(f'目标文件已存在, 执行覆盖')
                    else:
                        logger.info(f'目标文件已存在: {linux_file}')
            finally:
                sftp.close()
