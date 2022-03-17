import pymysql.cursors
from jlyPython.framework import readConfigFile

class Mysql(object):
    config = readConfigFile.ReadConfig()
    host = config.get_db("host")
    port = config.get_db("port")
    username = config.get_db("username")
    password = config.get_db("password")
    database = config.get_db("database")
    port = int(port)

    def get_db_conn(self):
        connection = pymysql.connect(host=self.host, port=self.port, user=self.username, passwd=self.password, db=self.database,
                                     charset='utf8', cursorclass=pymysql.cursors.DictCursor)

        return connection
        # try:
        #     cursor = connection.cursor()
        #     sql = sql
        #     cursor.execute(sql)
        #     results = cursor.fetchall()
        #     for data in results:
        #         return data
        #
        # except Exception:
        #     print("失败")
        # cursor.close()
        # connection.close()

    def query_db(self,sql):
        conn = Mysql().get_db_conn()  # 获取连接
        cur = conn.cursor()  # 建立游标
        cur.execute(sql)  # 执行sql
        result = cur.fetchall()  # 获取所有查询结果
        cur.close()  # 关闭游标
        conn.close()  # 关闭连接
        return result  # 返回结果

    # 封装更改数据库操作
    def change_db(self,sql):
        conn = Mysql().get_db_conn()  # 获取连接
        cur = conn.cursor()  # 建立游标
        try:
            cur.execute(sql)  # 执行sql
            conn.commit()  # 提交更改
        except Exception as e:
            conn.rollback()  # 回滚
        finally:
            cur.close()  # 关闭游标
            conn.close()  # 关闭连接

    # 封装常用数据库操作
    def check_user(self,sql):
        # 注意sql中''号嵌套的问题
        # sql = "select * from user where name = '{}'".format(name)
        result = Mysql().query_db(sql)
        return True if result else False

    def add_user(self,sql):
        # sql = "insert into user (name, passwd) values ('{}','{}')".format(name, password)
        Mysql().change_db(sql)

    def del_user(self,sql):
        # sql = "delete from user where name='{}'".format(name)
        Mysql().change_db(sql)



if __name__=='__main__':
    sql="select * from emplayee"
    p = Mysql().get_sql(sql)
    print(p)
