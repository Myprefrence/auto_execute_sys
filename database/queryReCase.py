from common.conn import *


class conn:

    def __init__(self,env):
        # Connect to the database
        self.connection = connects().conn_mysql()

        self.env = env

    def query_resCase(self, apply_no):
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = "select id,exec_model,data_tag from {}_res.t_case_apply_log where apply_no=%s".format(self.env)
                cursor.execute(sql, (apply_no, ))
                result = cursor.fetchone()
                return result
        finally:
            self.connection.close()

    def query_errorCase(self, apply_no):
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = "select apply_no,apply_id,biz_status,exec_model,data_tag from {}_res.t_case_error_log where apply_no = %s".format(self.env)
                cursor.execute(sql, (apply_no, ))
                result = cursor.fetchone()
                return result
        finally:
            self.connection.close()


if __name__ == '__main__':
    apply_no = ['XNAB032112060008720003']

    for i in apply_no:
        res_result = conn("test1").query_resCase(i)
        print("t_case_apply_log为: %s\n" % (res_result, ))

        res_errorRsult = conn("test1").query_errorCase(i)
        print("t_case_error_log为: %s\n" % (res_errorRsult, ))