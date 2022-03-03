from jenkins import Jenkins

from common import normal


class JenkinsServer:
    """
    @desc
    创建 Jenkins 连接对象
    简化构建以及一些信息查询的前置处理或操作
    也可以调用 JenkinsServer().jenkins_server 调用 Jenkins 模块方法

    :param server_url   jenkins 服务 url
    :param username     jenkins 登录用户
    :param password     jenkins 登录密码

    @func build                         执行构建
    @func is_building                   查询是否正在执行构建任务
    @func get_last_build_result         获取最后一次构建结果
    @func get_last_failure_build_number 获取最后一次失败构建的任务号
    @func get_build_console_output      获取构建任务的输出信息
    """

    def __init__(self, server_url=None, username=None, password=None):
        config = normal.get_config(r'config\utils.ini')

        self.server_url = config.get('jenkins', 'server_url') if server_url is None else server_url
        self.username = config.get('jenkins', 'username') if username is None else username
        self.password = config.get('jenkins', 'password') if password is None else password

        self.jenkins_server = Jenkins(url=self.server_url, username=self.username, password=self.password)

    def get_last_build_result(self, sys_name: str):
        # 获取指定系统的最后一次构建结果

        job_info = self.jenkins_server.get_job_info(sys_name)
        last_build = job_info['lastBuild']

        if last_build is not None:
            last_build_info = self.jenkins_server.get_build_info(sys_name, last_build['number'])

            return last_build_info['result']

    def is_building(self, sys_name: str):
        # 判断指定系统是否正在执行构建任务

        job_info = self.jenkins_server.get_job_info(sys_name)
        last_build = job_info['lastBuild']

        if last_build is not None:
            last_build_info = self.jenkins_server.get_build_info(sys_name, last_build['number'])
            return last_build_info['building']

    def build(self, sys_name: str, env_name: str, app_name: str, branch_name: str, params=None):
        """
        指定系统执行构建任务
        如果当前正在构建中, 返回 BUILDING
        如果最近一次构建失败, 返回 NOT_SUCCEED
        如果构建成功, 返回 SUCCESS
        """

        if self.is_building(sys_name):
            return 'BUILDING'
        if not self.get_last_build_result(sys_name) == 'SUCCESS':
            return 'NOT_SUCCEED'

        job_info = self.jenkins_server.get_job_info(sys_name)
        job_properties = job_info['property']

        group_name = None
        comp = None
        users = None
        code_name = None
        sonar = None
        git = None

        if params is None:

            for job_property in job_properties:
                if job_property['_class'] == 'hudson.model.ParametersDefinitionProperty':
                    params = job_property['parameterDefinitions']
                    break

            for param in params:
                default_value = param['defaultParameterValue']

                if default_value['name'] == 'groupName':
                    group_name = default_value['value']
                if default_value['name'] == 'comp':
                    comp = default_value['value']
                if default_value['name'] == 'users':
                    users = default_value['value']
                if default_value['name'] == 'codeName':
                    code_name = default_value['value']
                if default_value['name'] == 'sonar':
                    sonar = default_value['value']
                if default_value['name'] == 'git':
                    git = default_value['value']

        else:
            group_name = params['group_name']
            comp = params['comp']
            users = params['users']
            code_name = params['code_name']
            sonar = params['sonar']
            git = params['git']

        self.jenkins_server.build_job(
            name=sys_name,
            parameters={
                'groupName': group_name,
                'codeName': code_name,
                'comp': comp,
                'users': users,
                'sonar': sonar,
                'git': git,
                'BRANCH': branch_name,
                'Target': app_name,
                'Envior': env_name
            })

        return self.get_last_build_result(sys_name)

    def get_last_failure_build_number(self, sys_name: str):
        # 获取指定系统的最后一次构建失败任务号

        job_info = self.jenkins_server.get_job_info(sys_name)

        for param in job_info:
            if param == 'lastFailedBuild':
                last_failure_build = job_info['lastFailedBuild']

                if last_failure_build is None:
                    return None
                else:
                    return last_failure_build['number']

    def get_build_console_output(self, sys_name: str, build_id=None, get_failure=False):
        # 获取指定构建次号的输出信息
        # get_failure: 获取最近一次构建失败任务的输出信息

        if get_failure:
            build_id = self.get_last_failure_build_number(sys_name)
        if build_id is not None:
            return self.jenkins_server.get_build_console_output(sys_name, build_id)
