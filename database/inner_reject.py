from database.query_projectLine import *

class conn:

    def __init__(self, env):
        # Connect to the database
        self.connection = connects().conn_mysql()
        self.env = env

    def userid_prod_loan_risk_rej_cnt_90d(self, asset_org_no:str,business_type_code:str,platform_user_id:str,
                                          apply_result:str):
        # userid_self_prod_loan_risk_rej_cnt_90d 31
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = "select count(distinct id) from {}_res.t_case_apply_log where asset_org_no = %s and exec_model = '1' and" \
                      " json_extract(`req_data`, '$.business_type_code')=%s and (datediff(now(),apply_datetime)+1)<=90"\
                      " and platform_user_id = %s and apply_result = %s;".format(self.env)
                cursor.execute(sql, (asset_org_no, business_type_code, platform_user_id, apply_result))
                result = cursor.fetchall()
                return result
        finally:
            self.connection.close()

    def userid_grt_loan_risk_rej_cnt_90d(self, project_no:str, platform_user_id:str,apply_result:str):
        # userid_grt_loan_risk_rej_cnt_90d 32
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = "select count(distinct id) from {}_res.t_case_apply_log where exec_model = '1'" \
                      " and project_no = %s and (datediff(now(),apply_datetime)+1)<=90" \
                      " and platform_user_id = %s and apply_result = %s;".format(self.env)
                cursor.execute(sql, (project_no, platform_user_id, apply_result))
                result = cursor.fetchall()
                return result
        finally:
            self.connection.close()

    def userid_self_prod_last_loan_risk_rej_date(self, asset_org_no:str, business_type_code:str, platform_user_id:str,
                                                 apply_result: str):
        # userid_self_prod_last_loan_risk_rej_date 33

        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = "select max(apply_datetime) from {}_res.t_case_apply_log where asset_org_no = %s and" \
                      " json_extract(`req_data`, '$.business_type_code')=%s and exec_model = '1'" \
                      " and platform_user_id = %s and apply_result = %s;".format(self.env)
                # print(sql)
                cursor.execute(sql, (asset_org_no, business_type_code, platform_user_id, apply_result))
                result = cursor.fetchall()
                return result
        finally:
            self.connection.close()

    def userid_grt_last_loan_risk_rej_date(self, project_no:str, platform_user_id:str,apply_result:str):
        # userid_grt_last_loan_risk_rej_date 34

        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = "select max(apply_datetime) from {}_res.t_case_apply_log where exec_model = '1'" \
                      " and project_no = %s and (datediff(now(),apply_datetime)+1)<=90" \
                      " and platform_user_id = %s and apply_result = %s;".format(self.env)
                cursor.execute(sql, (project_no, platform_user_id, apply_result))
                result = cursor.fetchall()
                return result
        finally:
            self.connection.close()

    def phoneid_self_prod_loan_risk_rej_cnt_90d(self,asset_org_no:str,business_type_code, platform_mobile_id:str,apply_result:str):
        #phoneid_self_prod_loan_risk_rej_cnt_90d 35

        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = "select count(distinct id) from {}_res.t_case_apply_log where asset_org_no = %s and exec_model = '1' and" \
                      " json_extract(`req_data`, '$.business_type_code')=%s and (datediff(now(),apply_datetime)+1)<=90"\
                      " and platform_mobile_id = %s and apply_result = %s;".format(self.env)
                cursor.execute(sql, (asset_org_no, business_type_code,platform_mobile_id, apply_result))
                result = cursor.fetchall()
                return result
        finally:
            self.connection.close()

    def phoneid_grt_loan_risk_rej_cnt_90d(self, project_no:str, platform_mobile_id:str, apply_result):
        # phoneid_grt_loan_risk_rej_cnt_90d  36

        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = "select count(distinct id) from {}_res.t_case_apply_log where exec_model = '1'" \
                      " and project_no = %s and (datediff(now(),apply_datetime)+1)<=90" \
                      " and platform_mobile_id = %s and apply_result = %s;".format(self.env)
                cursor.execute(sql, (project_no, platform_mobile_id, apply_result))
                result = cursor.fetchall()
                return result
        finally:
            self.connection.close()

    def phoneid_self_prod_last_loan_risk_rej_date(self, asset_org_no:str, business_type_code:str,platform_mobile_id:str, apply_result):
        # phoneid_self_prod_last_loan_risk_rej_date 37

        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = "select max(apply_datetime) from {}_res.t_case_apply_log where asset_org_no = %s and" \
                      " json_extract(`req_data`, '$.business_type_code')=%s and exec_model = '1'" \
                      " and platform_mobile_id = %s and apply_result = %s;".format(self.env)
                cursor.execute(sql, (asset_org_no, business_type_code, platform_mobile_id, apply_result))
                result = cursor.fetchall()
                return result
        finally:
            self.connection.close()

    def phoneid_grt_last_loan_risk_rej_date(self, project_no:str, platform_mobile_id:str, apply_result):
        # phoneid_grt_last_loan_risk_rej_date 38

        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = "select max(apply_datetime) from {}_res.t_case_apply_log where exec_model = '1'" \
                      " and project_no = %s and (datediff(now(),apply_datetime)+1)<=90" \
                      " and platform_mobile_id = %s and apply_result = %s;".format(self.env)
                # print(sql)
                cursor.execute(sql, (project_no, platform_mobile_id, apply_result))
                result = cursor.fetchall()
                return result
        finally:
            self.connection.close()


if __name__ == '__main__':
    # env:环境
    env = "test1"

    # bis_type: 业务类型
    business_type_code = "0001"
    #审批结果
    apply_result = "D"
    #asset_org_no: 资产方
    asset_org_no = "360JR"

    #platform_user_id: user_id
    platform_user_id = "CI2112150000722439"
    #platform_mobile_id：mobile_id
    platform_mobile_id = "C3279109090144"
    #project_no: 项目号
    guarantee = projectLine().query_projectLine()

    feature = input("请输入特征编号：")
    if feature == "31":
        res_result = conn(env).userid_prod_loan_risk_rej_cnt_90d(asset_org_no, business_type_code, platform_user_id,
                                                      apply_result)
        for i in res_result:
            for j in i.values():
                print("统计借款申请单号数量为: %s" % (j,))





    elif feature == "32":
        sum = 0
        for project_code in guarantee:
            res_result = conn(env).userid_grt_loan_risk_rej_cnt_90d(project_code, platform_user_id, apply_result)
            for i in res_result:
                for j in i.values():
                    print("project_no：%s的结果数量为：%s" % (project_code, j))
                    sum += j

        print("统计借款申请单号数量为: %s" % (sum, ))


    elif feature == "33":
        time = []
        res_result = conn(env).userid_self_prod_last_loan_risk_rej_date(asset_org_no, business_type_code, platform_user_id, apply_result)
        for i in res_result:
            for j in i.values():
                if j is None:
                    print("未取到值")
                    pass
                else:
                    print("user_id为: %s的最大借款申请时间为: %s" % (platform_user_id, j,))




    elif feature == "34":
        time = []
        for project_no in guarantee:
            res_result = conn(env).userid_grt_last_loan_risk_rej_date(project_no, platform_user_id, apply_result)
            for i in res_result:
                for j in i.values():
                    print("最大借款申请时间为: %s" % (j,))
                    if j is None:
                        print("未取到值")
                        pass
                    else:
                        time.append(j)


        print("user_id为: %s的最大借款申请时间为: %s" % (platform_user_id, max(time),))




    elif feature == "35":
        res_result = conn(env).phoneid_self_prod_loan_risk_rej_cnt_90d(asset_org_no, business_type_code,platform_mobile_id,
                                                                       apply_result)
        for i in res_result:
            for j in i.values():
                print("统计借款申请单号数量为: %s" % (j,))




    elif feature == "36":
        sum = 0
        for project_code in guarantee:
            res_result = conn(env).phoneid_grt_loan_risk_rej_cnt_90d(project_code, platform_mobile_id,apply_result)
            for i in res_result:
                for j in i.values():
                    print("project_no：%s的结果数量为：%s" % (project_code, j))
                    sum += j

        print("统计借款申请单号数量为: %s" % (sum, ))


    elif feature == "37":

        res_result = conn(env).phoneid_self_prod_last_loan_risk_rej_date(asset_org_no, business_type_code, platform_mobile_id,
                                                                        apply_result)
        for i in res_result:
            for j in i.values():
                if j is None:
                    print("未取到值")
                    pass
                else:
                    print("platform_mobile_id: %s的最大借款申请时间为: %s" % (platform_mobile_id, j,))


    elif feature == "38":
        time = []
        for project_no in guarantee:
            res_result = conn(env).phoneid_grt_last_loan_risk_rej_date(project_no, platform_mobile_id, apply_result)
            for i in res_result:
                for j in i.values():
                    print("最大借款申请时间为: %s" % (j,))
                    if j is None:
                        print("未取到值")
                        pass
                    else:
                        time.append(j)

        print("platform_mobile_id: %s的最大借款申请时间为: %s" % (platform_mobile_id, max(time),))

    else:
        print("您输入的特征编号不存在！")






