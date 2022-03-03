from common.conn import *



class conn:

    def __init__(self,env):
        # Connect to the database
        self.connection = connects().conn_mysql()

        self.env = env

    def query_suspendLog(self, project_code: str, strategy_code: str, biz_status: str):
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"select suspend_id,apply_id,apply_no from {self.env}_res.t_case_suspend_log where suspend_id in ("\
                      f"select id from {self.env}_res.t_suspend_config_info where project_code = %s and strategy_code =%s and biz_status=%s)"
                cursor.execute(sql, (project_code, strategy_code,biz_status))
                result = cursor.fetchall()
                return result
        finally:
            self.connection.close()

    def query_project(self, project_code):
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = "select id, code,version from {}_res.t_project_info where code = %s".format(self.env)
                cursor.execute(sql, (project_code, ))
                result = cursor.fetchall()
                return result
        finally:
            self.connection.close()

    def query_strategy(self, strategy_code):
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = "select id,strategy_code,version from {}_res.t_strategy_info where strategy_code = %s".format(self.env)
                cursor.execute(sql, (strategy_code, ))
                result = cursor.fetchall()
                return result
        finally:
            self.connection.close()


if __name__ == '__main__':
    # '卡件状态：init-待生效；active-生效中；offline-已下线；inactive-未生效'
    suspend_result = conn("test1").query_suspendLog("A002", "X008", "offline")
    for i in suspend_result:
        if i is None:
            print("查询无结果,未创建卡件")
        else:
            print("卡件查询案件结果为: %s" % (i, ))
