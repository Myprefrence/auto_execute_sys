import random
import string
import time
import threading




class insert_sql:

    def random_digits(self):
        ran_str1 = ''.join(random.sample(string.digits, 8))
        ran_str2 = ''.join(random.sample(string.digits, 8))
        ran_str3 = ''.join(random.sample(string.digits, 8))
        ran_str = ran_str1 + ran_str2 + ran_str3
        return ran_str

    def loanReqNo(self):
        ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        now_time = str(time.time())
        now_time = now_time.split('.')
        ran_str = ran_str + now_time[0]

        return ran_str

    def insert_thread(self):
        id = "XNAC" + self.random_digits()
        loan_order_id = "XNAC" + self.random_digits()
        asset_loan_order_no = self.loanReqNo()
        cust_no = "XNAE" + self.random_digits()
        cap_loan_order_id = "XNAC" + self.random_digits()


        sql = "INSERT INTO `xna_test1_cbs`.`t_commission_record`(`id`, `loan_order_id`, `loan_amt`," \
              " `asset_loan_order_no`, `cust_no`, `overdue_type`, `asset_org_no`, `project_no`, `data_type`, `statistics_date`, `create_datetime`," \
              " `update_datetime`, `created_by`, `updated_by`, `cap_loan_order_id`, `loan_success_date`," \
              " `need_rpy_total_amt`, `need_rpy_principal`, `need_rpy_interest`, `need_rpy_overdue_fee`," \
              " `rpy_total_amt`, `rpy_principal`, `rpy_interest`, `rpy_overdue_fee`, `commission_rpy_total_amt`," \
              " `commission_rpy_principal`, `commission_rpy_interest`, `commission_rpy_overdue_fee`, `project_name`," \
              " `collection_agency_code`, `collection_agency_name`, `channel`, `cust_name`, `compensation_total_amt`," \
              " `compensation_principal`, `compensation_interest`, `compensation_overdue_fee`, `remaining_total_amt`," \
              " `remaining_principal`, `commission_amt`, `overdue_days`, `max_history_overdue_days`, `last_repay_datetime`," \
              " `match_commission_date`, `send_commission_date`, `commission_status`, `reach_status`, `status_desc`, " \
              "`repay_after_commission`, `full_compensation`, `order_settle`, `commission_batch_id`, `update_status`)" \
              " VALUES ('{}', '{}', 700.00, '{}'," \
              " '{}', 'overdu90', '360JR', '1001', 'order', '20211123', '2021-11-23 15:18:05'," \
              " '2021-12-14 09:30:06', NULL, NULL, '{}', '2021-07-22 06:59:57', 843.60, 699.96," \
              " 143.64, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, '360_哈密银行', NULL, NULL, NULL," \
              " '刘史珐g1', 209.73, 174.99, 2.40, 32.34, 843.60, 699.96, 843.60, 114, 114, NULL, '2021-11-23 15:18:05'," \
              " NULL, 'WAIT_SEND', NULL, NULL, 0, 0, 0, NULL, 'success');".format(id,loan_order_id,asset_loan_order_no,cust_no,cap_loan_order_id)

        print(sql)

        with open("sql.txt","a",encoding='utf-8') as f:
            f.write(sql + "\n")
            f.close()

    def main(self,thread_number):
        threadpool = []
        for i in range(thread_number):
            th = threading.Thread(target=self.insert_thread, args=())
            threadpool.append(th)
        for th in threadpool:
            th.start()
            time.sleep(1)
        for th in threadpool:
            threading.Thread.join(th)


if __name__ == '__main__':
    insert_sql().main(1000)

    # print(insert_sql().random_digits())