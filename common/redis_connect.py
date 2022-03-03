import datetime
import random

import redis

from common import normal


class RedisConnect:
    """
    @desc
    创建 redis 连接池, 获取一个 redis 连接对象
    可以直接通过 RedisConnect().conn 调用 Redis 模块方法
    也可以通过 RedisConnect 实例对象调用封装好的方法

    :param env              测试环境
    :param db               redis连接数据库
    :param host             redis连接地址, 为空则读取配置文件
    :param password         redis连接密码, 为空则读取配置文件
    :param decode_responses 是否解析响应结果

    @func z_get_record_by_time      获取 z-set key 中一个时间范围内的记录, 简化数据处理步骤
    @func z_count_record_by_time    获取 z-set key 中一个时间范围内的记录总数, 简化数据处理步骤
    @func z_range_random_add        向 z-set key 中指定时间范围内指定次数插入指定格式的随机数据
    """

    def __init__(self, env: str, db: int, host=None, port=6379, password=None, decode_responses=True):
        config = normal.get_config(r'config\utils.ini')

        if env not in ('test1', 'test2'):
            raise Exception(f'不存在的测试环境信息: {env}')

        host = config.get(env, 'host') if host is None else host
        port = config.get(env, 'port') if port is None else port
        password = config.get(env, 'password') if password is None else password

        self.pool = redis.ConnectionPool(
            host=host,
            port=int(port),
            password=password,
            db=db,
            decode_responses=decode_responses
        )
        self.conn = redis.Redis(connection_pool=self.pool)

    @staticmethod
    def get_min_and_max_timestamp(index_time: object, time_diff=0, max_border=False):
        if type(index_time) not in (int, str, datetime.datetime):
            raise Exception(f'不正确的起始时间数据类型: {index_time}')
        if isinstance(index_time, str):
            index_time = datetime.datetime.strptime(index_time, '%Y-%m-%d %H:%M:%S')
        if isinstance(index_time, datetime.datetime):
            index_time = normal.get_timestamp(index_time)

        min_timestamp = 0
        max_timestamp = 0
        range_time = index_time + time_diff * 1000

        if range_time != index_time:
            if range_time > index_time:
                if not max_border:
                    range_time -= 1
                min_timestamp = index_time
                max_timestamp = range_time

            if range_time < index_time:
                if not max_border:
                    index_time -= 1
                min_timestamp = range_time
                max_timestamp = index_time
        else:
            min_timestamp = index_time
            max_timestamp = index_time

        return {'min_timestamp': min_timestamp, 'max_timestamp': max_timestamp}

    @staticmethod
    def get_z_key_value_name(timestamp: int or str, prefix_1='', prefix_2='', suffix=''):
        result = f'{prefix_1}{timestamp}'
        if prefix_2 is not None:
            result = f'{result}@{prefix_2}{timestamp}'
        if suffix is not None:
            result = f'{result}#{suffix}'
        return result

    def z_get_record_by_time(self, key: str, index_time: object, time_diff=0, max_border=False, reverse=False):
        """
        获取 z-set key 中一个时间范围内的记录, 对调用 zrangebysocre() 方法的前处理步骤进行了简化

        key         键路径
        index_time  起始时间, 可以传入时间戳, 日期时间及日期时间格式的字符串
        time_diff   与 index_time 的时间差, 单位秒
                    例如 index_time 后一个小时, 则 time_diff = 60 * 60
                    例如 index_time 前一个小时, 则 time_diff = -60 * 60
        max_border  是否包含边界值, 例如 2022-01-01 00:00:00 ~ 2022-01-02 00:00:00
                    查询范围为 1640966400000 ~ 1641052800000, 不包含边界值则为 1640966400000 ~ 1641052799999
        reverse     查询结果是否倒序排序

        以上述为例, 不包含边界值, 执行
                    z_get_record_by_time(key=xx, index_time='2022-01-01 00:00:00', time_diff=60 * 60 * 24)
        或者
                    z_get_record_by_time(key=xx, index_time='2021-01-02 00:00:00', time_diff=-60 * 60 *24)
        或者
                    z_get_record_by_time(key=xx, index_time=1640966400000, time_diff=60 * 60 * 3600)
        可以得到一样的结果
        """

        timestamp = self.get_min_and_max_timestamp(index_time=index_time, time_diff=time_diff, max_border=max_border)

        if reverse:
            return self.conn.zrevrangebyscore(name=key, max=timestamp['max_timestamp'], min=timestamp['min_timestamp'])
        else:
            return self.conn.zrangebyscore(name=key, min=timestamp['min_timestamp'], max=timestamp['max_timestamp'])

    def z_count_record_by_time(self, key: str, index_time: object, time_diff=0, max_border=False):
        """
        获取 z-set key 中一个时间范围内的记录总数, 逻辑同上, 对调用 zcount() 方法的前处理步骤进行了简化
        """

        timestamp = self.get_min_and_max_timestamp(index_time=index_time, time_diff=time_diff, max_border=max_border)
        return self.conn.zcount(name=key, min=timestamp['min_timestamp'], max=timestamp['max_timestamp'])

    def z_range_random_add(self, key: str, index_time: object, add_times=1, time_diff=0, max_border=False, prefix_1='',
                           prefix_2=None, suffix=None):
        """
        向一个 z-set key 进行指定时间范围内指定次数的随机造数, 简化造数的前处理步骤

        key         键路径
        index_time  起始时间, 见上 z_get_record_by_time()
        add_times   造数次数, 默认为 1 次
                    当造数次数等于 1 时, 造数会随机选择最大和最小边界时间戳作为 score
                    当造数次数大于 1 时, 会往两个边界值至少造一条数据
        time_diff   与 index_time 的时间差, 单位秒, 见上 z_get_record_by_time()
        max_border  是否包含边界值, 见上 z_get_record_by_time()

        prefix      拼接时间戳
        suffix      拼接末尾
                    使用方法, 例如 timestamp = 1640966400000:

                    prefix_1 = 'XNAA', prefix_2 = 'XNAB', suffix = 'AB01'
                        -> value = XNAA1640966400000@XNAB1640966400000#AB01

                    prefix_1 = 'XNAA', prefix_2 = 'XNAB', suffix = ''
                        -> value = XNAA1640966400000@XNAB1640966400000      suffix 为空时不拼接末尾

                    prefix_1 = 'XNAA', 'prefix_2 = '', suffix = 'AB01'
                        -> value = XNAA1640966400000#AB01                   prefix_2 为空时则直接拼接 prefix_1 和 suffix

                    prefix_1 = '', prefix_2 = 'XNAB', suffix = 'AB01'
                        -> value = 1640966400000@XNAB1640966400000#AB01     prefix_1 即使为空, 仍会在开头拼接时间戳

        假设一个使用场景, 需要向 key=xx 下随机插入 100 条 score 在 [2022-01-01 00:00:00, 2022-01-01 12:00:00] 区间的数据.
        且 value 格式为 XNACxxxxx#xx, 则执行

                    z_range_random_add(
                        key=xx,
                        add_times=100,
                        index_time='2022-01-01 00:00:00',
                        time_diff=60 * 60 * 12,
                        prefix_1='XNAC',
                        suffix='xx'
                    )
        """
        timestamp = self.get_min_and_max_timestamp(index_time=index_time, time_diff=time_diff, max_border=max_border)

        if add_times >= 2:
            min_timestamp = timestamp['min_timestamp']
            max_timestamp = timestamp['max_timestamp']

            data = {
                self.get_z_key_value_name(
                    min_timestamp, prefix_1=prefix_1, prefix_2=prefix_2, suffix=suffix): min_timestamp,
                self.get_z_key_value_name(
                    max_timestamp, prefix_1=prefix_1, prefix_2=prefix_2, suffix=suffix): max_timestamp
            }

            random_timestamp_set = set()
            for i in range(add_times - 2):
                while True:
                    random_timestamp = random.randint(min_timestamp, max_timestamp)
                    if random_timestamp in random_timestamp_set:
                        continue
                    else:
                        random_timestamp_set.add(random_timestamp)
                        break

                data[self.get_z_key_value_name(
                    random_timestamp, prefix_1=prefix_1, prefix_2=prefix_2, suffix=suffix)] = random_timestamp

            return self.conn.zadd(name=key, mapping=data)

        else:
            random_timestamp = timestamp[random.choice('min_timestamp', 'max_timestamp')]
            data = {
                self.get_z_key_value_name(
                    random_timestamp, prefix_1=prefix_1, prefix_2=prefix_2, suffix=suffix): random_timestamp
            }

            return self.conn.zadd(name=key, mapping=data)


