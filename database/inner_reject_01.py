from common.conn import *

class conn:

    def __init__(self, xn, env):
        # Connect to the database
        self.connection = connects().conn_mysql()
        self.env = env
        self.xn = xn

    def userid_prod_loan_risk_rej_cnt_90d(self, bis_type:str,asset_org_no:str,id_no_platform_id:str):
        # userid_self_prod_loan_risk_rej_cnt_90d 31
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = "select count(distinct id) from {}_{}_cbs.t_loan_order where order_status='LOAN_FAIL' " \
                      "and bis_type_id=%s and asset_org_no=%s and channel like '%%res%%' and (datediff(now()," \
                      "loan_apply_datetime)+1)<=90 and order_status_desc like '%%担保公司审核不通过%%' and" \
                      f" cust_no in (select cust_no from {self.xn}_{self.env}_eam.t_cust_info where id_no_platform_id= %s)".format(self.xn, self.env)
                cursor.execute(sql, (bis_type, asset_org_no, id_no_platform_id))
                result = cursor.fetchall()
                return result
        finally:
            self.connection.close()

    def userid_grt_loan_risk_rej_cnt_90d(self, id_no_platform_id:str, project_no:str):
        # userid_grt_loan_risk_rej_cnt_90d 32
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = "select count(distinct id) from {}_{}_cbs.t_loan_order where order_status='LOAN_FAIL'"\
                      f"and channel like '%%res%%' and cust_no in (select cust_no from {self.xn}_{self.env}_eam.t_cust_info where id_no_platform_id= %s) and" \
                      " (datediff(now(),loan_apply_datetime)+1)<=90 and project_no = %s".format(self.xn, self.env)
                cursor.execute(sql, (id_no_platform_id, project_no))
                result = cursor.fetchall()
                return result
        finally:
            self.connection.close()

    def userid_self_prod_last_loan_risk_rej_date(self, bis_type:str, asset_org_no:str, id_no_platform_id:str):
        # userid_self_prod_last_loan_risk_rej_date 33

        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = "select max(loan_apply_datetime) from {}_{}_cbs.t_loan_order where  order_status='LOAN_FAIL'" \
                      " and bis_type_id= %s and asset_org_no= %s and channel like '%%res%%'" \
                      " and cust_no in" \
                     f" (select cust_no from {self.xn}_{self.env}_eam.t_cust_info where id_no_platform_id= %s);".format(self.xn, self.env)
                print(sql)
                cursor.execute(sql, (bis_type, asset_org_no, id_no_platform_id))
                result = cursor.fetchall()
                return result
        finally:
            self.connection.close()

    def userid_grt_last_loan_risk_rej_date(self, id_no_platform_id:str, project_no:str):
        # userid_grt_last_loan_risk_rej_date 34

        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = "select max(loan_apply_datetime) from {}_{}_cbs.t_loan_order where order_status='LOAN_FAIL' and order_status_desc like '%%担保公司审核不通过%%' and" \
                      f" channel like '%%res%%' and cust_no in (select cust_no from {self.xn}_{self.env}_eam.t_cust_info where id_no_platform_id= %s) and project_no = %s;".format(self.xn,self.env)
                cursor.execute(sql, (id_no_platform_id, project_no))
                result = cursor.fetchall()
                return result
        finally:
            self.connection.close()

    def phoneid_self_prod_loan_risk_rej_cnt_90d(self, bis_type:str, asset_org_no:str, mobile_no:str):
        #phoneid_self_prod_loan_risk_rej_cnt_90d 35

        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"select count(distinct id) from {self.xn}_{self.env}_cbs.t_loan_order where order_status='LOAN_FAIL' and" \
                      " bis_type_id=%s and asset_org_no=%s" \
                      " and channel like '%%res%%' and (datediff(now(),loan_apply_datetime)+1)<=90 and" \
                      f" and cust_no = (select cust_no from {self.xn}_{self.env}_eam.t_asset_cust_info" \
                      " where mobile_no = %s);"
                cursor.execute(sql, (bis_type, asset_org_no, mobile_no))
                result = cursor.fetchall()
                return result
        finally:
            self.connection.close()

    def phoneid_grt_loan_risk_rej_cnt_90d(self, project_no:str, mobile_no:str):
        # phoneid_grt_loan_risk_rej_cnt_90d  36

        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"select count(distinct id) from {self.xn}_{self.env}_cbs.t_loan_order where order_status='LOAN_FAIL' and" \
                      " project_no = %s" \
                      " and channel like '%%res%%' and (datediff(now(),loan_apply_datetime)+1)<=90 and" \
                      f" and cust_no = (select cust_no from {self.xn}_{self.env}_eam.t_asset_cust_info" \
                      " where mobile_no = %s);"
                cursor.execute(sql, (project_no, mobile_no))
                result = cursor.fetchall()
                return result
        finally:
            self.connection.close()

    def phoneid_self_prod_last_loan_risk_rej_date(self, bis_type:str, asset_org_no:str, mobile_no:str):
        # phoneid_self_prod_last_loan_risk_rej_date 37

        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"select max(loan_apply_datetime) from {self.xn}_{self.env}_cbs.t_loan_order where order_status='LOAN_FAIL' and" \
                      " bis_type_id=%s and asset_org_no=%s" \
                      " and channel like '%%res%%' and (datediff(now(),loan_apply_datetime)+1)<=90 and" \
                      f" and cust_no = (select cust_no from {self.xn}_{self.env}_eam.t_asset_cust_info" \
                      " where mobile_no = %s);"
                cursor.execute(sql, (bis_type, asset_org_no, mobile_no))
                result = cursor.fetchall()
                return result
        finally:
            self.connection.close()

    def phoneid_grt_last_loan_risk_rej_date(self, project_no:str, mobile_no:str):
        # phoneid_grt_last_loan_risk_rej_date 38

        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"select max(loan_apply_datetime) from {self.xn}_{self.env}_cbs.t_loan_order where order_status='LOAN_FAIL' and" \
                      " project_no = %s" \
                      " and channel like '%%res%%' and (datediff(now(),loan_apply_datetime)+1)<=90 and" \
                      f" and cust_no = (select cust_no from {self.xn}_{self.env}_eam.t_asset_cust_info" \
                      " where mobile_no = %s);"
                cursor.execute(sql, (project_no, mobile_no))
                result = cursor.fetchall()
                return result
        finally:
            self.connection.close()

if __name__ == '__main__':
    # env:环境
    env = "test2"
    # en:虚拟环境
    xn = ["xna", "xnb"]
    # bis_type: 业务类型
    bis_type = "0001"
    #asset_org_no: 资产方
    asset_org_no = "360JR"
    project_no = "1001"
    #mobile:手机号码
    mobile = ""
    #cust_no: 客户号
    id_no_platform_id = "CI2112090000670471"
    #project_no: 项目号
    guarantee = ["1001", "6006", "6013", "1002", "W001", "W002"]
    feature = input("请输入特征编号：")
    if feature == "31":
        sum = 0
        for x in xn:
            res_result = conn(x, env).userid_prod_loan_risk_rej_cnt_90d(bis_type, asset_org_no, id_no_platform_id)
            for i in res_result:
                for j in i.values():
                    sum += j
        print("统计借款申请单号数量为: %s" % (sum,))



    elif feature == "32":
        sum = 0
        for x in xn:
            for project_no in guarantee:
                res_result = conn(x, env).userid_grt_loan_risk_rej_cnt_90d(id_no_platform_id, project_no)
                for i in res_result:
                    for j in i.values():
                        sum += j


        print("统计借款申请单号数量为: %s" % (sum, ))


    elif feature == "33":
        time = []
        for x in xn:
            res_result = conn(x, env).userid_self_prod_last_loan_risk_rej_date(bis_type, asset_org_no,id_no_platform_id)
            for i in res_result:
                for j in i.values():
                    print("最大借款申请时间为: %s" % (j,))
                    if j is None:
                        print("未取到值")
                        pass
                    else:
                        time.append(j)

        print("user_id为: %s的最大借款申请时间为: %s" % (id_no_platform_id, max(time),))





    elif feature == "34":
        time = []
        for x in xn:
            for project_no in guarantee:
                res_result = conn(x, env).userid_grt_last_loan_risk_rej_date(id_no_platform_id, project_no)
                for i in res_result:
                    for j in i.values():
                        print("最大借款申请时间为: %s" % (j,))
                        if j is None:
                            print("未取到值")
                            pass
                        else:
                            time.append(j)

        print("user_id为: %s的最大借款申请时间为: %s" % (id_no_platform_id, max(time),))


    elif feature == "35":
        res_result = conn(xn, env).phoneid_self_prod_loan_risk_rej_cnt_90d(bis_type, asset_org_no, mobile)
        for i in res_result:
            for j in i.values():
                print("统计借款申请单号数量为: %s" % (j, ))



    elif feature == "36":
        res_result = conn(xn, env).phoneid_grt_loan_risk_rej_cnt_90d(mobile, project_no)
        for i in res_result:
            for j in i.values():
                print("统计借款申请单号数量为: %s" % (j,))


    elif feature == "37":
        res_result = conn(xn, env).phoneid_self_prod_last_loan_risk_rej_date(bis_type, asset_org_no, mobile)
        for i in res_result:
            for j in i.values():
                print("最大借款申请时间为: %s" % (j, ))


    elif feature == "38":
        res_result = conn(xn, env).phoneid_grt_last_loan_risk_rej_date(project_no, mobile)
        for i in res_result:
            for j in i.values():
                print("最大借款申请时间为: %s" % (j, ))


    else:
        print("您输入的特征编号不存在！")






