import configparser
import os
import time

import redis

# root_dir = os.path.dirname(os.path.abspath('.'))
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
configPath = root_dir + "\config\config.ini"
# cf = configparser.ConfigParser()
cf = configparser.RawConfigParser()
cf.read(configPath)  # 拼接得到config.ini文件的路径，直接使用

secs = cf.sections()  # 获取文件中所有的section(一个配置文件中可以有多个配置，如数据库相关的配置，邮箱相关的配置，每个section由[]包裹，即[section])，并以列表的形式返回


# options = cf.options("Mysql")  # 获取某个section名为Mysql-Database所对应的键
# print(options)
# items = cf.items("Mysql")  # 获取section名为Mysql-Database所对应的全部键值对
# print(items)

class redisConn:

    def __init__(self, env):
        if env == "test1":
            self.host = cf.get("Redis", "test1_host")
            self.password = cf.get("Redis", "test1_password")
        elif env == "test2":
            self.host = cf.get("Redis", "test2_host")
            self.password = cf.get("Redis", "test2_password")

        self.db = cf.get("Redis", "db")
        self.port = cf.get("Redis", "port")

    def connect_redis(self):

        redis_pool = redis.ConnectionPool(
            host=self.host,
            password=self.password,
            port=int(self.port),
            db=int(self.db)
        )
        redis_conn = redis.Redis(connection_pool=redis_pool)
        # redis_conn.set('name1', 'zhangsansan')
        # print(redis_conn.get("name"))

        return redis_conn

    def get_timestamp(self, datetime_str):
        return int(time.mktime(time.strptime(datetime_str, '%Y-%m-%d %H:%M:%S'))) * 1000


if __name__ == '__main__':
    path = "risk:res:case:dyna_var:completed_approval:daily:project_code:asset_org_no:211220:A002:360JR"
    value = "XNAA032111220009490001@XNAB032111220007800002"
    key = path + ":" + value

    score = int(time.time() * 1000)
    map = {
        value: score

    }
    conn = redisConn().connect_redis()

    time1 = redisConn().get_timestamp('2021-11-23 21:03:25')
    time2 = redisConn().get_timestamp('2021-12-23 21:03:26')

    # Zcount 命令用于计算有序集合中指定分数区间的成员数量。分数值在 min 和 max 之间的成员的数量
    print(conn.zcount(path, min=time1, max=time2))

    # 添加元素并排序
    # result = conn.zadd(name=path, mapping=map)

    # 删除元素

    # r.zrem("aa","v2")

    # 返回区间元素并排序 desc=False 时就从小到大取,反之.
    # print(str(conn.zrange(path, 0, 2, desc=True)))

    # zcard key：返回key的基数，key不存在时返回0
    # print(conn.zcard(path))

    # Zscore 命令返回有序集中，成员的分数值。 如果成员元素不是有序集 key 的成员，或 key 不存在，返回 None
    print(conn.zscore(path, value=value))

    # Zrevrank 命令返回有序集中成员的排名。其中有序集成员按分数值递减(从大到小)排序
    # print(conn.zrevrank(path, value=value))

    # Zrank 返回有序集中指定成员的排名。其中有序集成员按分数值递增(从小到大)顺序排列
    # print(conn.zrank(path,value))

    # Zlexcount 命令在计算有序集合中指定字典区间内成员数量
    # print(conn.zlexcount(path, min="-", max="+"))
