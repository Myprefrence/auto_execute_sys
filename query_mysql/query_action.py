from common.conn import *
from common.conn_adb import *
from common.conn import *

class Action:

    def __init__(self, mysql, xn, env, asset_org_no='', bis_type_id=''):
        # Connect to the database
        if mysql == "adb":
            self.connection = connect_adb().conn_mysql()
        elif mysql == "jly":
            self.connection = connects().conn_mysql()
        self.env = env
        self.xn = xn
        self.asset_org_no = asset_org_no
        self.bis_type_id = bis_type_id

    def query_action_47_1(self, id_no):
        '''查询关联的订单号、还款状态、当前周期'''
        '''特征变量47查询repay_settle = 0的最大逾期天数'''
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"select repay_settle, loan_order_id,current_period, project_no from {self.xn}_{self.env}_cbs.t_repay_plan where" \
                      f" loan_order_id in (SELECT id FROM {self.xn}_{self.env}_cbs.t_loan_order WHERE cust_no in (select cust_no from" \
                      f" {self.xn}_{self.env}_eam.t_cust_info where id_no_platform_id=%s) AND project_no IN " \
                      f"( SELECT project_no FROM {self.env}_nls.t_project_line WHERE project_line = 'guarantee' " \
                      f"and status='1') AND order_status IN ('ON_REPAYMENT', 'SETTLED'));"
                cursor.execute(sql, (id_no, ))
                result = cursor.fetchall()
                return result
        finally:
            self.connection.close()

    def query_action_47_2(self, current_period, loan_order_id):
        '''如果repay_title=1时，查询还款计划表最大逾期天数'''
        '''userid_self_prod_max_overdue_days'''
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"SELECT max(DATEDIFF(last_rpy_datetime,schedule_date)) from {self.xn}_{self.env}_cbs.t_repay_plan where " \
                      f"current_period=%s and loan_order_id=%s;"
                cursor.execute(sql, (current_period, loan_order_id, ))
                result = cursor.fetchall()

                return result
        finally:
            self.connection.close()

    def query_action_47_3(self, current_period:int, loan_order_id:str):
        '''如果repay_title=0时，查询还款计划表的schedule_total,schedule_date'''
        '''userid_self_prod_max_overdue_days'''
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"select schedule_total,schedule_date from {self.xn}_{self.env}_cbs.t_repay_plan where current_period=%s and " \
                      f"loan_order_id=%s;"
                cursor.execute(sql, (current_period, loan_order_id, ))
                result = cursor.fetchall()
                return result
        finally:
            self.connection.close()

    def query_action_47_4(self, current_period:int, loan_order_id:str):
        '''如果repay_title=0时，查询还款记录中总已还款金额，最大还款时间'''
        '''userid_self_prod_max_overdue_days'''
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"select sum(rpy_total_amt),max(rpy_datetime) from {self.xn}_{self.env}_cbs.t_repay_record where rpy_period=%s and " \
                      f"loan_order_id=%s;"
                cursor.execute(sql, (current_period, loan_order_id, ))
                result = cursor.fetchall()

                return result
        finally:
            self.connection.close()

    def query_action_47_5(self, current_period, loan_order_id):
        '''如果实还金额小于应还金额时，当前时间减应还时间'''
        '''userid_self_prod_max_overdue_days'''
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"SELECT max(DATEDIFF(now(),schedule_date)) from {self.xn}_{self.env}_cbs.t_repay_plan where current_period=%s and " \
                      f"loan_order_id=%s;"
                cursor.execute(sql, (current_period, loan_order_id, ))
                result = cursor.fetchall()

                return result
        finally:
            self.connection.close()

    def query_action_47_6(self, rpy_datetime, current_period, loan_order_id):
        '''如果实还金额大于等于于应还金额时，实还时间减应还时间'''
        '''userid_self_prod_max_overdue_days'''
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"SELECT max(DATEDIFF(%s,schedule_date)) from {self.xn}_{self.env}_cbs.t_repay_plan where current_period=%s and " \
                      f"loan_order_id=%s;"
                cursor.execute(sql, (rpy_datetime, current_period, loan_order_id ))
                result = cursor.fetchall()

                return result
        finally:
            self.connection.close()

    def query_action_48(self, id_no):
        '''特征变量48查询repay_settle = 0的最大逾期天数'''
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = "SELECT max(datediff( NOW(), schedule_date )) FROM (SELECT a.id_no,a.asset_loan_order_no," \
                      "a.order_status,a.project_no,b.schedule_date,b.last_rpy_datetime,b.repay_settle FROM (SELECT id_no," \
                      f"asset_loan_order_no,order_status,project_no FROM {self.xn}_{self.env}_cbs.t_loan_order WHERE cust_no in " \
                      f"(select cust_no from {self.xn}_{self.env}_eam.t_cust_info where id_no=%s) AND " \
                      f"asset_org_no = %s and bis_type_id = %s AND order_status IN ( 'ON_REPAYMENT', 'SETTLED' )) " \
                      f"AS a LEFT JOIN {self.xn}_{self.env}_cbs.t_repay_plan AS b ON a.asset_loan_order_no = b.asset_loan_order_no ) " \
                      "AS c WHERE repay_settle = 0;"
                cursor.execute(sql, (id_no, self.asset_org_no, self.bis_type_id))

                result = cursor.fetchall()
                result = result[0]['max(datediff( NOW(), schedule_date ))']
                return result
        finally:
            self.connection.close()

    def query_action_48_1(self, id_no):
        '''根据用户id查询repay_settle, loan_order_id,current_period,project_no'''
        '''userid_self_prod_max_overdue_days'''
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"select repay_settle, loan_order_id,current_period,project_no from {self.xn}_{self.env}_cbs.t_repay_plan " \
                      f"where loan_order_id in (SELECT id from {self.xn}_{self.env}_cbs.t_loan_order where order_status " \
                      f"in ('ON_REPAYMENT','SETTLED') and `type`= 'CBS' and bis_type_id=%s and asset_org_no=%s and cust_no " \
                      f"in (select cust_no from {self.xn}_{self.env}_eam.t_cust_info where id_no_platform_id=%s));"
                cursor.execute(sql, (self.bis_type_id, self.asset_org_no, id_no, ))
                result = cursor.fetchall()
                # result = result[0]['max(datediff( NOW(), schedule_date ))']
                return result
        finally:
            self.connection.close()

    def query_action_48_2(self, current_period, loan_order_id):
        '''如果repay_title=1时，查询还款计划表最大逾期天数'''
        '''userid_self_prod_max_overdue_days'''
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"SELECT max(DATEDIFF(last_rpy_datetime,schedule_date)) from {self.xn}_{self.env}_cbs.t_repay_plan where " \
                      f"current_period=%s and loan_order_id=%s;"
                cursor.execute(sql, (current_period, loan_order_id, ))
                result = cursor.fetchall()

                return result
        finally:
            self.connection.close()

    def query_action_48_3(self, current_period:int, loan_order_id:str):
        '''如果repay_title=0时，查询还款计划表的schedule_total,schedule_date'''
        '''userid_self_prod_max_overdue_days'''
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"select schedule_total,schedule_date from {self.xn}_{self.env}_cbs.t_repay_plan where current_period=%s and " \
                      f"loan_order_id=%s;"
                cursor.execute(sql, (current_period, loan_order_id, ))
                result = cursor.fetchall()
                return result
        finally:
            self.connection.close()

    def query_action_48_4(self, current_period:int, loan_order_id:str):
        '''如果repay_title=0时，查询还款记录中总已还款金额，最大还款时间'''
        '''userid_self_prod_max_overdue_days'''
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"select sum(rpy_total_amt),max(rpy_datetime) from {self.xn}_{self.env}_cbs.t_repay_record where rpy_period=%s and " \
                      f"loan_order_id=%s;"
                cursor.execute(sql, (current_period, loan_order_id, ))
                result = cursor.fetchall()

                return result
        finally:
            self.connection.close()

    def query_action_48_5(self, current_period, loan_order_id):
        '''如果实还金额小于应还金额时，当前时间减应还时间'''
        '''userid_self_prod_max_overdue_days'''
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"SELECT max(DATEDIFF(now(),schedule_date)) from {self.xn}_{self.env}_cbs.t_repay_plan where current_period=%s and " \
                      f"loan_order_id=%s;"
                cursor.execute(sql, (current_period, loan_order_id, ))
                result = cursor.fetchall()

                return result
        finally:
            self.connection.close()

    def query_action_48_6(self, rpy_datetime, current_period, loan_order_id):
        '''如果实还金额大于等于于应还金额时，实还时间减应还时间'''
        '''userid_self_prod_max_overdue_days'''
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"SELECT max(DATEDIFF(%s,schedule_date)) from {self.xn}_{self.env}_cbs.t_repay_plan where current_period=%s and " \
                      f"loan_order_id=%s;"
                cursor.execute(sql, (rpy_datetime, current_period, loan_order_id ))
                result = cursor.fetchall()

                return result
        finally:
            self.connection.close()


    def query_action_49_1(self, id_no):
        '''查询关联的订单号、还款状态、当前周期'''
        '''特征变量49查询repay_settle = 0的最大逾期天数'''
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"select repay_settle, loan_order_id,current_period, project_no from {self.xn}_{self.env}_cbs.t_repay_plan where" \
                      f" loan_order_id in (SELECT id FROM {self.xn}_{self.env}_cbs.t_loan_order WHERE cust_no in (select cust_no from" \
                      f" {self.xn}_{self.env}_eam.t_cust_info where id_no_platform_id=%s) AND project_no IN " \
                      f"( SELECT project_no FROM {self.env}_nls.t_project_line WHERE project_line = 'guarantee' " \
                      f"and status='1') AND order_status IN ('ON_REPAYMENT', 'SETTLED'));"
                cursor.execute(sql, (id_no, ))
                result = cursor.fetchall()
                return result
        finally:
            self.connection.close()


    def query_action_49_2(self, current_period, loan_order_id):
        '''如果repay_title=1时，查询还款计划表最大逾期天数'''
        '''userid_self_prod_max_overdue_days'''
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"SELECT max(DATEDIFF(last_rpy_datetime,schedule_date)) from {self.xn}_{self.env}_cbs.t_repay_plan where " \
                      f"current_period=%s and loan_order_id=%s;"
                cursor.execute(sql, (current_period, loan_order_id, ))
                result = cursor.fetchall()

                return result
        finally:
            self.connection.close()

    def query_action_49_3(self, current_period:int, loan_order_id:str):
        '''如果repay_title=0时，查询还款计划表的schedule_total,schedule_date'''
        '''userid_self_prod_max_overdue_days'''
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"select schedule_total,schedule_date from {self.xn}_{self.env}_cbs.t_repay_plan where current_period=%s and " \
                      f"loan_order_id=%s;"
                cursor.execute(sql, (current_period, loan_order_id, ))
                result = cursor.fetchall()
                return result
        finally:
            self.connection.close()

    def query_action_49_4(self, current_period:int, loan_order_id:str):
        '''如果repay_title=0时，查询还款记录中总已还款金额，最大还款时间'''
        '''userid_self_prod_max_overdue_days'''
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"select sum(rpy_total_amt),max(rpy_datetime) from {self.xn}_{self.env}_cbs.t_repay_record where rpy_period=%s and " \
                      f"loan_order_id=%s;"
                cursor.execute(sql, (current_period, loan_order_id, ))
                result = cursor.fetchall()

                return result
        finally:
            self.connection.close()

    def query_action_49_5(self, current_period, loan_order_id):
        '''如果实还金额小于应还金额时，当前时间减应还时间'''
        '''userid_self_prod_max_overdue_days'''
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"SELECT max(DATEDIFF(now(),schedule_date)) from {self.xn}_{self.env}_cbs.t_repay_plan where current_period=%s and " \
                      f"loan_order_id=%s;"
                cursor.execute(sql, (current_period, loan_order_id, ))
                result = cursor.fetchall()

                return result
        finally:
            self.connection.close()

    def query_action_49_6(self, rpy_datetime, current_period, loan_order_id):
        '''如果实还金额大于等于于应还金额时，实还时间减应还时间'''
        '''userid_self_prod_max_overdue_days'''
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"SELECT max(DATEDIFF(%s,schedule_date)) from {self.xn}_{self.env}_cbs.t_repay_plan where current_period=%s and " \
                      f"loan_order_id=%s;"
                cursor.execute(sql, (rpy_datetime, current_period, loan_order_id ))
                result = cursor.fetchall()

                return result
        finally:
            self.connection.close()

    def query_action_50_0(self, id_no, project_no):
        '''特征变量50查询repay_settle = 0的最大逾期天数'''
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"SELECT max(datediff(rp.last_repay_date, rp.need_repay_date)) FROM {self.xn}_{self.env}_pls.t_order_info oi," \
                      f"{self.xn}_{self.env}_pls.t_repay_plan_detail rp WHERE oi.cust_no in (select cust_no from " \
                      f"{self.xn}_{self.env}_eam.t_cust_info where id_no=%s) AND oi.order_no = rp.order_no AND " \
                      "oi.project_no = %s AND rp.overdue_sign ='Y' AND rp.settled_sign = 'Y';"
                cursor.execute(sql, (id_no, project_no))
                result = cursor.fetchall()
                result = result[0]['max(datediff(rp.last_repay_date, rp.need_repay_date))']

                return result
        finally:
            self.connection.close()

    def query_action_50_1(self, id_no, project_no):
        '''特征变量50查询repay_settle = 0的最大逾期天数'''
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"SELECT max(datediff(now(), rp.need_repay_date)) FROM {self.xn}_{self.env}_pls.t_order_info oi," \
                      f"{self.xn}_{self.env}_pls.t_repay_plan_detail rp WHERE oi.cust_no in (select cust_no from " \
                      f"{self.xn}_{self.env}_eam.t_cust_info where id_no=%s) AND oi.order_no = rp.order_no AND " \
                      "oi.project_no = %s AND rp.overdue_sign ='Y' AND rp.settled_sign = 'N';"
                cursor.execute(sql, (id_no, project_no))
                result = cursor.fetchall()
                result = result[0]['max(datediff(now(), rp.need_repay_date))']

                return result
        finally:
            self.connection.close()

    def query_action_51(self, id_no):
        '''特征变量51查询总的实还款金额'''
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"SELECT sum(rpy_total_amt) FROM {self.xn}_{self.env}_cbs.t_repay_record t,(SELECT id_no,asset_org_no," \
                      f"bis_type_id,order_status,asset_loan_order_no FROM {self.xn}_{self.env}_cbs.t_loan_order where cust_no in " \
                      f"(select cust_no from {self.xn}_{self.env}_eam.t_cust_info where id_no=%s) and asset_org_no " \
                      f"= %s and bis_type_id = %s and order_status in ('ON_REPAYMENT','SETTLED')) as a  where " \
                      "t.asset_loan_no = a.asset_loan_order_no;"
                cursor.execute(sql, (id_no, self.asset_org_no, self.bis_type_id))
                result = cursor.fetchall()
                result = result[0]['sum(rpy_total_amt)']

                return result
        finally:
            self.connection.close()

    def query_action_52(self, id_no):
        '''特征变量52查询总的实还款金额'''
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"SELECT sum(rpy_total_amt) FROM	{self.xn}_{self.env}_cbs.t_repay_record t,(SELECT id_no,asset_org_no," \
                      f"bis_type_id,order_status,asset_loan_order_no FROM {self.xn}_{self.env}_cbs.t_loan_order where cust_no in " \
                      f"(select cust_no from {self.xn}_{self.env}_eam.t_cust_info where id_no=%s) AND project_no " \
                      f"IN ( SELECT project_no FROM {self.env}_nls.t_project_line WHERE project_line = 'guarantee' and status='1') " \
                      f"and order_status in ('ON_REPAYMENT','SETTLED')) as a  where t.asset_loan_no = a.asset_loan_order_no;"
                cursor.execute(sql, (id_no, ))
                result = cursor.fetchall()
                result = result[0]['sum(rpy_total_amt)']
                return result
        finally:
            self.connection.close()

    def query_action_54(self, id_no):
        '''特征变量54统计自然月的还款金额大于0的实还款月'''
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"SELECT count(distinct(concat(SUBSTR(rpy_datetime,1,4),SUBSTR(rpy_datetime,6,2)))) FROM " \
                      f"{self.xn}_{self.env}_cbs.t_repay_record t,(SELECT id_no," \
                      f"asset_org_no,bis_type_id,order_status,asset_loan_order_no FROM {self.xn}_{self.env}_cbs.t_loan_order where " \
                      f"cust_no in (select cust_no from {self.xn}_{self.env}_eam.t_cust_info where id_no=%s) and " \
                      f"asset_org_no = %s and bis_type_id = %s and order_status in ('ON_REPAYMENT','SETTLED')) " \
                      f"as a  where t.asset_loan_no = a.asset_loan_order_no and t.rpy_total_amt > 0;"
                cursor.execute(sql, (id_no, self.asset_org_no, self.bis_type_id))
                result = cursor.fetchall()

                result = result[0]['count(distinct(concat(SUBSTR(rpy_datetime,1,4),SUBSTR(rpy_datetime,6,2))))']

                return result
        finally:
            self.connection.close()

    def query_action_55_0(self, id_no):
        '''特征变量55统计自然月的还款金额大于0的实还款月-融担'''
        results = []
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"SELECT distinct(concat(SUBSTR(rpy_datetime,1,4),SUBSTR(rpy_datetime,6,2))) FROM {self.xn}_{self.env}_cbs.t_repay_record t,(SELECT id_no," \
                      f"asset_org_no,bis_type_id,order_status,asset_loan_order_no FROM {self.xn}_{self.env}_cbs.t_loan_order where " \
                      f"cust_no in (select cust_no from {self.xn}_{self.env}_eam.t_cust_info where id_no=%s) and " \
                      f"order_status in ('ON_REPAYMENT','SETTLED')) " \
                      f"as a  where t.asset_loan_no = a.asset_loan_order_no and t.rpy_total_amt > 0;"
                cursor.execute(sql, (id_no, ))
                result = cursor.fetchall()

                for i in range(0, len(result)):
                    result_s = result[i]['(concat(SUBSTR(rpy_datetime,1,4),SUBSTR(rpy_datetime,6,2)))']
                    results.append(result_s)

                return results
        finally:
            self.connection.close()

    def query_action_55_1(self, id_no):
        '''特征变量55统计自然月的还款金额大于0的实还款月-通道'''
        results = []
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"SELECT distinct(SUBSTR(rr.repay_date,1,6)) FROM {self.xn}_{self.env}_pls.t_order_info oi," \
                      f"{self.xn}_{self.env}_pls.t_repay_record rr WHERE oi.cust_no in (select cu.cust_no from " \
                      f"{self.xn}_{self.env}_eam.t_cust_info as cu where cu.id_no=%s) AND oi.order_no = rr.order_no;"
                cursor.execute(sql, (id_no, ))
                result = cursor.fetchall()

                for i in range(0, len(result)):
                    result_s = result[i]['(SUBSTR(rr.repay_date,1,6))']
                    results.append(result_s)

                return results
        finally:
            self.connection.close()

    def query_action_56(self, id_no):
        '''特征变量56计算project_line=‘passage’的项目的放款金额'''
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"SELECT sum(loan_principal) FROM {self.xn}_{self.env}_pls.t_order_info  WHERE cust_no in (select cust_no " \
                      f"from {self.xn}_{self.env}_eam.t_cust_info where id_no=%s) AND project_no IN ( SELECT " \
                      f"project_no FROM {self.env}_nls.t_project_line WHERE project_line = 'passage' and status='1');"
                cursor.execute(sql, (id_no, ))
                result = cursor.fetchall()

                result = result[0]['sum(loan_principal)']

                return result
        finally:
            self.connection.close()

    def query_action_58(self, id_no):
        '''特征变量58统计project_line=‘passage’的项目的放款成功的资产方编号'''
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"SELECT count(distinct(asset_org_no)) FROM {self.xn}_{self.env}_pls.t_order_info  WHERE cust_no in (select cust_no " \
                      f"from {self.xn}_{self.env}_eam.t_cust_info where id_no=%s) AND project_no IN ( SELECT " \
                      f"project_no FROM {self.env}_nls.t_project_line WHERE project_line = 'passage' and status='1');"
                cursor.execute(sql, (id_no, ))
                result = cursor.fetchall()

                result = result[0]['count(distinct(asset_org_no))']

                return result
        finally:
            self.connection.close()

    def query_action_59(self, id_no):
        '''特征变量58统计project_line=‘guarantee’的项目的放款成功的最大放款金额'''
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"SELECT max(loan_amt) FROM {self.xn}_{self.env}_cbs.t_loan_order  WHERE cust_no in (select cust_no from " \
                      f"{self.xn}_{self.env}_eam.t_cust_info where id_no=%s) AND project_no IN ( SELECT " \
                      f"project_no FROM {self.env}_nls.t_project_line WHERE project_line = 'guarantee' and status='1') AND " \
                      f"order_status IN ( 'ON_REPAYMENT', 'SETTLED' );"
                cursor.execute(sql, (id_no, ))

                result = cursor.fetchall()

                result = result[0]['max(loan_amt)']

                return result
        finally:
            self.connection.close()


if __name__ == '__main__':
    load_id = "XNAC092201211933110004020091"
    mysql = "adb"
    xn = "dw"
    env = "test1"
    id_no = "CI2201210000800084"
    asset_org_no ="360JR"
    bis_type_id = "0001"
    action = Action(mysql, xn, env,asset_org_no, bis_type_id)
    # print(action.query_action_47_0("110101196403078051"))
    print(action.query_action_48_1(id_no))