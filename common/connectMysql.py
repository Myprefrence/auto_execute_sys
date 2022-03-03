from common.conn import *


class conn:

    def __init__(self, xn, env):
        # Connect to the database
        self.connection = connects().conn_mysql()

        self.env = env
        self.xn = xn

    def query_orderID(self, order_no):
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = "select id from {}_{}_cbs.t_loan_order where asset_loan_order_no=%s".format(self.xn, self.env)
                cursor.execute(sql, (order_no,))
                result = cursor.fetchone()
                return result
        finally:
            self.connection.close()

    def query_rmsSatus(self, order_id):
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = "select * from  {}_{}_rms.t_risk_request_info where loan_order_id=%s".format(self.xn, self.env)
                cursor.execute(sql, (order_id,))
                result = cursor.fetchone()
                return result
        finally:
            self.connection.close()

    def query_res(self, order_id):

        try:
            # with connection.cursor() as cursor:
            #     # Create a new record
            #     sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
            #     cursor.execute(sql, ('webmaster@python.org', 'very-secret'))
            #
            # # connection is not autocommit by default. So you must commit to save
            # # your changes.
            # connection.commit()

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"select apply_no,id,exec_model,data_tag from {self.env}_res.t_case_apply_log where biz_no =" \
                      f"(select risk_log_id from {self.xn}_{self.env}_rms.t_risk_monitor_log where loan_order_id =" \
                      f"(select id from {self.xn}_{self.env}_cbs.t_loan_order where asset_loan_order_no = %s) and channel_code=%s)".format()
                # print(sql)
                cursor.execute(sql, (order_id, 'res'))
                result = cursor.fetchone()
                return result
        finally:
            self.connection.close()

    def query_resCase(self, apply_no):
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = "select id,data_tag from {}_res.t_case_apply_log where apply_no=%s".format(self.env)
                cursor.execute(sql, (apply_no,))
                result = cursor.fetchone()
                return result
        finally:
            self.connection.close()


if __name__ == '__main__':
    param = ['loan111a800-DDA']
    apply_id = []
    for i in param:
        # cbs_result = conn().query_orderID(i)
        # rms_result = conn().query_rmsSatus(cbs_result["id"])
        # print("order_no为: %s, order_id为: %s, rms结果为: %s\n" % (i, cbs_result, rms_result))

        res_result = conn("xna", "test2").query_res(i)
        if res_result is None:
            continue
        else:
            apply_id.append(res_result["id"])

        print("order_no为: %s, res结果为: %s\n" % (i, res_result))

    print("apply_id数据为: %s" % (apply_id,))
