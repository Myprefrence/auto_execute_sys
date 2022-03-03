from common.conn import *


class conn:

    def __init__(self,env):
        # Connect to the database
        self.connection = connects().conn_mysql()

        self.env = env

    def query_resCaseCount(self, project_code, exec_model,data_tag):
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # 利用to_days函数查询今天的数据：select * from 表名 where to_days(时间字段名) = to_days(now());
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = "select apply_no,id,project_code,exec_model,data_tag,create_datetime from {}_res.t_case_apply_log where" \
                      " project_code = %s and exec_model = %s and data_tag= %s and to_days(create_datetime) = to_days(CURDATE())".format(self.env)

                cursor.execute(sql, (project_code, exec_model, data_tag))
                result = cursor.fetchall()
                return result
        finally:
            self.connection.close()


if __name__ == '__main__':
    #执行模式 '执行模式：online-在线:1  offline-离线:2
    project_code = "A002"
    CaseCount = conn("test1").query_resCaseCount(project_code, "2", "2.0")
    count = 0
    for i in CaseCount:
        if len(i) == 0:
            print("查询当天的案件数为零")

        else:
            print("根据查询返回res详情结果为: %s" % (i,))
            count += 1

    print("当天data_tag为%s的案件统计数量为: %s\n" % (project_code, count))



