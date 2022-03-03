from common.conn import *

class conn:

    def __init__(self,env):
        # Connect to the database
        self.connection = connects().conn_mysql()

        self.env = env

    def query_ecwResult(self, case_id):
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = "select case_id,exec_model,status,mq_status, success_status,data_tag from {}_ecw.t_request_info where case_id = %s".format(self.env)
                cursor.execute(sql, (case_id, ))
                result = cursor.fetchall()
                return result
        finally:
            self.connection.close()


if __name__ == '__main__':
    # 执行模式 1：在线 2：离线'
    # status '完成状态 0-初始状态 1-处理中 2-处理成功 3-返回成功
    # mq_status 'MQ状态 0-默认 1-待处理 2-处理完成 3-处理异常'
    # success_status '结果状态 0-初始状态 1--处理成功 2-处理失败'
    case_id = ['XNAA032112020010190091', 'XNAA032112020010190090', 'XNAA032112020010220135', 'XNAA032112020010220136']

    for i in case_id:
        ecw_result = conn("test1").query_ecwResult(i)
        if len(ecw_result) == 0:
            print("查询ecw无返回结果，请检查case_id是否有效，case_id: %s" % (i, ))
        else:
            print("查询ecw返回结果: %s" % (ecw_result, ))