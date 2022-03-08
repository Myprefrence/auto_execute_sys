"""
风控系统数据库操作部分
"""

from database import db


# 查询策略信息
def get_strategy_info_by_code(env: str, strategy_code: str):
    return db.select(f'select * from {env}_res.t_strategy_info where '
                     f'strategy_code = "{strategy_code}";')


# 查询策略最新归档信息
def get_strategy_latest_archive_info(env: str, strategy_code: str):
    return db.select(f'select * from {env}_res.t_strategy_info_archives where '
                     f'strategy_code = "{strategy_code}"'
                     f'order by create_datetime desc limit 1;')


# 修改策略归档信息中的提交者
def update_strategy_submitter(env: str, archive_id: str):
    db.modify(f'update {env}_res.t_strategy_info_archives set '
              f'submit_by = "tester" where '
              f'id = "{archive_id}";')


# 查询策略关联支持项目
def get_strategy_ref_project(env: str, strategy_code: str):
    return db.select(f'select * from {env}_res.t_strategy_project_ref where '
                     f'strategy_code = "{strategy_code}" and '
                     f'enable = "Y" and '
                     f'create_datetime = ('
                     f'select max(create_datetime) from {env}_res.t_strategy_project_ref where '
                     f'strategy_code = "{strategy_code}" and '
                     f'enable = "Y");', size=-1)


# 查询策略输出变量
def get_strategy_output_variable(env: str, strategy_code: str, version: str):
    return db.select(f'select * from {env}_res.t_var_ref_info where '
                     f'object_code = "{strategy_code}" and '
                     f'object_version = "{version}" and '
                     f'object_type = "strategy_outbound" and '
                     f'enable = "Y" and '
                     f'create_datetime = ('
                     f'select max(create_datetime) from {env}_res.t_var_ref_info where '
                     f'object_code = "{strategy_code}" and '
                     f'object_version = "{version}" and '
                     f'object_type = "strategy_outbound" and '
                     f'enable = "Y");', size=-1)


# 查询项目信息
def get_project_info_by_code(env: str, project_code: str):
    return db.select(f'select * from {env}_res.t_project_info where '
                     f'code = "{project_code}";')


# 查询项目最新归档信息
def get_project_latest_archive_info(env: str, project_code: str):
    return db.select(f'select * from {env}_res.t_project_info_archives where '
                     f'code = "{project_code}" '
                     f'order by create_datetime desc limit 1;')


# 修改项目归档信息中的提交者
def update_project_submitter(env: str, archive_id: str):
    db.modify(f'update {env}_res.t_project_info_archives set '
              f'create_by = "tester" where '
              f'id = "{archive_id}";')


# 查询最近一条有效的卡件项目记录
def get_valid_suspend_info(env: str, project_code: str):
    return db.select(f'select * from {env}_res.t_suspend_config_info where '
                     f'project_code = "{project_code}" and '
                     f'biz_status in ("init", "active") '
                     f'order by create_datetime desc limit 1;')
