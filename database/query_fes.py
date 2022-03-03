from common.conn import *

class conn:

    def __init__(self, env):
        self.connection = connects().conn_mysql()
        self.env = env

    def query_fesResult(self, case_id):
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = "select case_id,exec_model,mq_status,data_tag from {}_fes.t_request_info where case_id = %s".format(self.env)
                cursor.execute(sql, (case_id, ))
                result = cursor.fetchall()
                return result
        finally:
            self.connection.close()


if __name__ == '__main__':
    # 执行模式 1：在线 2：离线'
    # mq_status 'MQ 0-默认 1-待处理 2-处理完成 3-处理异常'
    case_id = ['XNAA032112020010220036', 'XNAA032112020010220034', 'XNAA032112020010190053', 'XNAA032112020010190052', 'XNAA032112020010220035']

    for i in case_id:
        fes_result = conn("test1").query_fesResult(i)
        if len(fes_result) == 0:
            print("查询fes无返回结果，请检查case_id是否有效或者查看ecw是否调用成功，case_id: %s" % (i, ))

        else:
            print("查询fes返回结果: %s" % (fes_result, ))