from common.conn import *


class conn:

    def __init__(self,env):
        # Connect to the database
        self.connection = connects().conn_mysql()

        self.env = env

    def query_offlineRisk(self, task_code):
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = f"select task_code,case_no, case_id, data_tag from {self.env}_res.t_task_offline_log where task_code= %s;"
                cursor.execute(sql, (task_code, ))
                result = cursor.fetchall()
                return result
        finally:
            self.connection.close()


if __name__ == '__main__':
    task_code = ['120601']
    offline_apply_no = []
    offline_apply_id = []

    for i in task_code:
        offlineTask_result = conn("test1").query_offlineRisk(i)
        for j in offlineTask_result:
            offline_apply_no.append(j["case_no"])
            offline_apply_id.append(j["case_id"])
            print("resOffline结果为: %s\n" % (j,))

    print("offline_apply_no为: %s\n" %(offline_apply_no, ))
    print("offline_apply_id为: %s\n" % (offline_apply_id,))

