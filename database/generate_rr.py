from common.conn import *
import requests
import time
import datetime



class generate:
    def __init__(self, xn, env):
        # Connect to the database
        self.connection = connects().conn_mysql()
        self.env = env
        self.xn = xn
        self.headers = {"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8"}
        self.s = requests.sessions

    def login(self):
        '''登录'''
        data = {
            "uname": "risk",
            "pwd": "risk@2021&&"
        }

        url = "https://oms{}.jiuliyuntech.com/sso-oms/loginByAjax".format(self.env)

        response = self.s.post(url=url, data=data, headers=self.headers).json()

        print(response["msg"])

    def query_cap_plan(self, order_no):
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"select * from {self.xn}_{self.env}_cap.t_cap_repay_plan_detail where loan_id=(select cap_loan_order_no from" \
                      f" {self.xn}_{self.env}_cbs.t_loan_order where asset_loan_order_no = %s);"
                cursor.execute(sql, (order_no, ))
                result = cursor.fetchall()
                return result
        finally:
            self.connection.close()

    def query_cbs_plan(self, order_no):
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = "select schedule_total,schedule_principal,schedule_interest,schedule_overdue_fee,schedule_other_fee " \
                      "from {}_{}_cbs.t_repay_plan where asset_loan_order_no = %s;"\
                    .format(self.xn, self.env)
                cursor.execute(sql, (order_no, ))
                result = cursor.fetchall()
                return result
        finally:
            self.connection.close()

    def update_cap_plan(self, schedule_date, order_no, current_period):
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"update {self.xn}_{self.env}_cap.t_cap_repay_plan_detail set schedule_date = %s where" \
                      f" loan_id=(select cap_loan_order_no from {self.xn}_{self.env}_cbs.t_loan_order where " \
                      f"asset_loan_order_no = %s) and current_period= %s;"

                cursor.execute(sql, (schedule_date, order_no, current_period))
                # print(sql)

            self.connection.commit()

        finally:
            self.connection.close()

    def update_cbs_plan(self, rpy_total_amt, rpy_principal, rpy_interest, rpy_overdue_fee,rpy_other_fee,repay_settle,
                        last_rpy_datetime, asset_loan_order_no, current_period):
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = "update {}_{}_cbs.t_repay_plan set rpy_total_amt=%s,rpy_principal=%s,rpy_interest=%s," \
                      "rpy_overdue_fee=%s,rpy_other_fee=%s,repay_settle=%s,last_rpy_datetime=%s where" \
                      " asset_loan_order_no=%s and current_period=%s;".format(self.xn, self.env)

                cursor.execute(sql, (rpy_total_amt, rpy_principal, rpy_interest, rpy_overdue_fee,rpy_other_fee,
                                     repay_settle, last_rpy_datetime, asset_loan_order_no, current_period, ))
                # print(sql)

            self.connection.commit()

        finally:
            self.connection.close()


if __name__ == '__main__':
     cbs_result = generate("xna", "test1").query_cbs_plan("h5W2OUQL1640611353")

     current_period = 1
     for date in cbs_result:
         schedule_date = date["schedule_date"]
         schedule_date = schedule_date + " " + "00:00:00"
         schedule_date = datetime.datetime.strptime(schedule_date, '%Y-%m-%d %H:%M:%S')
         generate("xna", "test1").update_cap_plan(schedule_date, "h5W2OUQL1640611353", current_period)
         current_period += 1


