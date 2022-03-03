# 1.String set 设置单个键值
# set(name, value, ex=None, px=None, nx=False, xx=False)

# ex：过期时间（秒），时间到了后redis会自动删除
# px：过期时间（毫秒），时间到了后redis会自动删除。ex、px二选一即可
# nx：如果设置为True，则只有name不存在时，当前set操作才执行
# xx：如果设置为True，则只有name存在时，当前set操作才执行

# 2.String get 获取单个值

# v = redis_conn.get('name_1')
# print(v)


# 3.String mset 设置多个键值

# mset(*args, **kwargs)
#
# redis_conn.mset(name_1= 'Zarten_1', name_2= 'Zarten_2')
# 或者
#
# name_dict = {
#     'name_4' : 'Zarten_4',
#     'name_5' : 'Zarten_5'
# }
# redis_conn.mset(name_dict)
#
#
# 4.String mget 获取多个值
#
# mget(keys, *args)
#
# m = redis_conn.mget('name_1', 'name_2')
# #m = redis_conn.mget(['name_1', 'name_2']) 也行
# print(m)