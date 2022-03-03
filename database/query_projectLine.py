from common.conn import *

class projectLine:

    def __init__(self):
        # Connect to the database
        self.connection = connects().conn_mysql()

    def query_projectLine(self):
        project_no = []
        try:

            with self.connection.cursor() as cursor:
                # Read a single record
                # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                sql = "select distinct(project_no) from test2_nls.t_project_line where  project_line = 'guarantee';"
                cursor.execute(sql, ())
                result = cursor.fetchall()
                if result != None:
                    for i in result:
                        project_n = i["project_no"]
                        project_no.append(project_n)

                else:
                    print("查询无结果")


                return project_no
        finally:
            self.connection.close()


if __name__ == '__main__':
    ''
