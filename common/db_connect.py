import pymysql
from dbutils.pooled_db import PooledDB

from common import normal


class DBConnect:
    """
    @desc
    创建数据库连接池, 获取一个类型为 PyMySQL 的连接对象
    再通过连接对象创建一个存储类型为 Dict 的游标对象
    简化游标对象的相关操作, 只需传入 SQL 即可
    也可以通过 DBConnect().cursor 调用 PyMySQL 模块方法

    :param host     数据库连接地址, 为空则读取配置文件
    :param port     数据库连接端口, 为空则读取配置文件
    :param username 数据库连接用户名, 为空则读取配置文件
    :param password 数据库连接密码, 为空则读取配置文件

    @func select    根据 SQL 查询数据库记录
    @func modify    根据 SQL 执行数据库的增删改操作
    """

    def __init__(self, host=None, port=None, username=None, password=None):
        config = normal.get_config(r'config\utils.ini')

        host = config.get('database', 'host') if host is None else host
        port = config.get('database', 'port') if port is None else port
        username = config.get('database', 'username') if username is None else username
        password = config.get('database', 'password') if password is None else password

        pool = PooledDB(creator=pymysql, host=host, port=int(port), user=username, passwd=password, charset='utf8')
        self.conn = pool.connection()
        self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)

    # 查询操作:
    # size=1: 返回一条查询结果
    # size=-1: 返回全部查询结果
    # size>1: 返回指定数量查询结果
    def select(self, sql: str, size=1):
        self.cursor.execute(sql)

        if size == 1:
            return self.cursor.fetchone()
        elif size == -1:
            return self.cursor.fetchall()
        else:
            return self.cursor.fetchmany(size=size)

    # 更新操作, 包含新增, 删除, 修改
    def modify(self, sql: str):
        self.cursor.execute(sql)
        self.conn.commit()  # 失败会自动回滚, 此处不主动捕捉异常, 方便报错时观察
