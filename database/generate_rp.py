from common.conn import *
import requests
import random
import string



class generate:

    def __init__(self, xn, env):
        # Connect to the database
        self.connection = connects().conn_mysql()
        self.env = env
        self.xn = xn
        self.headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
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

    def query_order(self, order_no):
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = "select id,asset_org_no,asset_org_name,cust_no,loan_period,project_no from {}_{}_cbs.t_loan_order where asset_loan_order_no=%s;".format(self.xn, self.env)
                cursor.execute(sql, (order_no, ))
                result = cursor.fetchall()
                return result
        finally:
            self.connection.close()

    def repay_plan(self, re_id, order_id, order_no, cap_loan_order_no,loan_term,loan_t,loan_date,rey_total,rpy_principal,rpy_interest,
                   create_datetime, update_datetime, asset_org_no, asset_org_name, cust_no, cust_name, project_no, loanAmt):
        '''还款计划'''

        try:
            with self.connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO {}_{}_cbs.t_repay_plan(`id`, `loan_order_id`, `asset_loan_order_no`," \
                      " `cap_loan_order_no`, `total_period_cnt`, `current_period`, `repay_settle`, `schedule_date`," \
                      " `schedule_total`, `schedule_principal`, `schedule_interest`, `schedule_overdue_fee`," \
                      " `schedule_other_fee`, `rpy_total_amt`, `rpy_principal`, `rpy_interest`, `rpy_overdue_fee`," \
                      " `rpy_other_fee`, `last_rpy_datetime`, `marketing_reduction`, `compliance_reduction`," \
                      " `other_reduction`, `status`, `type`, `version`, `create_datetime`, `update_datetime`," \
                      " `created_by`, `updated_by`, `asset_org_no`, `asset_org_name`, `cust_no`, `cust_name`," \
                      " `project_no`, `project_name`, `channel`, `loan_amt`, `grace_date`, `schedule_gua_fee`," \
                      " `rpy_gua_fee`, `schedule_service_fee`, `rpy_service_fee`, `schedule_late_fee`, `rpy_late_fee`," \
                      " `schedule_compound_interest`, `rpy_compound_interest`) VALUES (%s," \
                      " %s, %s, %s," \
                      " %s, %s, 0, %s, %s, %s, %s, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00," \
                      " NULL, 0.00, 0.00, NULL, NULL, 'CBS', 0, %s, %s, 'sys'," \
                      " '345', %s, %s, %s, %s, %s, '360-阳光消金'," \
                      " NULL, %s, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);"\
                    .format(self.xn, self.env)

                cursor.execute(sql, (re_id, order_id, order_no, cap_loan_order_no,
                            loan_term, loan_t, loan_date, rey_total, rpy_principal, rpy_interest, create_datetime,
                            update_datetime, asset_org_no, asset_org_name, cust_no, cust_name, project_no, loanAmt))

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            self.connection.commit()

        finally:
            self.connection.close()


if __name__ == '__main__':
    order = "gnuvw8rQ1640582243"
    print(generate("xna", "test1").query_order(order))

