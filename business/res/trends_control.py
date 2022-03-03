from common.connectRedis import *
import random
import datetime
import string


class trendsControl:

    def __init__(self, env, project_code: str,
                  asset_org_no=None,
                  product_code=None, inner_var=None, before_time=None):
        self.conn_redis = redisConn(env).connect_redis()
        self.project_code = project_code
        self.asset_org_no = asset_org_no
        self.product_code = product_code
        self.inner_var = inner_var
        self.before_time = before_time


    def get_timestamp(self, datetime_str):
        return int(time.mktime(time.strptime(datetime_str, '%Y-%m-%d %H:%M:%S'))) * 1000

    def re_time(self, datetime_int):
        re = (datetime.datetime.now() - datetime.timedelta(minutes=self.before_time)).__format__('%Y-%m-%d %H:%M:%S')
        re = re.split(' ')
        re = re[0].split('-')
        re = '21' + re[1] + re[2]
        re = int(re)
        return re

    def split_time(self, min_t):
        min_year = min_t.year
        min_year = (str(min_year))[2:]
        min_month = min_t.month
        min_day = min_t.day
        day_time = min_year + str(min_month) + str(min_day)
        return day_time

    def split_path(self, path:str, min, max):
        min_time = self.split_time(min)
        max_time = self.split_time(max)
        new_path = path.replace(max_time, min_time)

        return new_path

    def random_param(self):
        param1 = ''.join(str(i) for i in random.sample(string.digits, 8))
        param2 = ''.join(str(i) for i in random.sample(range(0, 9), 9))
        param3 = str(random.randint(0, 9))
        projece_c = 'XNAA' + param2 + param1 + param3
        project_n = 'XNAB' + param1 + param2 + param3

        return projece_c, project_n

    def get_path(self, now_time: int, flag=1):
        index = []

        if self.asset_org_no is not None:
            if self.inner_var == None:
                if flag == 0:
                    time1 = now_time
                    time2 = now_time - 1
                    # path = "risk:res:case:dyna_var:completed_approval:daily:" \
                    #        "project_code:asset_org_no:{}:{}:{}".format(time1, self.project_code, self.asset_org_no)
                    path1 = "risk:res:case:dyna_var:completed_approval:daily:" \
                            "project_code:asset_org_no:{}:{}:{}".format(time2, self.project_code, self.asset_org_no)

                    # index.append(path)
                    index.append(path1)

                elif flag == 1:
                    if self.before_time != None:
                        time = self.re_time(self.before_time)

                    else:
                        time = now_time

                    path = "risk:res:case:dyna_var:completed_approval:daily:" \
                           "project_code:asset_org_no:{}:{}:{}".format(time, self.project_code, self.asset_org_no)

                    index.append(path)

                else:
                    print("flag只能输入1或0")
            else:
                if flag == 0:
                    time1 = now_time
                    time2 = now_time - 1
                    # path = "risk:res:case:dyna_var:completed_approval:daily:" \
                    #        "project_code:asset_org_no:{}:{}:{}".format(time1, self.project_code, self.asset_org_no)
                    path = "risk:res:case:dyna_var:completed_approval:daily:" \
                            "project_code:asset_org_no:{}:{}:{}:var_inner:{}".format(time2, self.project_code,
                                                                                     self.asset_org_no, self.inner_var)
                    path1 = "risk:res:case:dyna_var:completed_approval:daily:" \
                            "project_code:asset_org_no:{}:{}:{}".format(time2, self.project_code, self.asset_org_no)

                    index.append(path)
                    index.append(path1)

                elif flag == 1:
                    if self.before_time != None:
                        time = self.re_time(self.before_time)

                    else:
                        time = now_time
                    path = "risk:res:case:dyna_var:completed_approval:daily:" \
                           "project_code:asset_org_no:{}:{}:{}:var_inner:{}".format(time, self.project_code,
                                                                                    self.asset_org_no, self.inner_var)
                    path1 = "risk:res:case:dyna_var:completed_approval:daily:" \
                            "project_code:asset_org_no:{}:{}:{}".format(time, self.project_code, self.asset_org_no)

                    index.append(path)
                    index.append(path1)

                else:
                    print("flag只能输入1或0")

        elif self.product_code is not None:
            if self.inner_var == None:
                if flag == 0:
                    time1 = now_time
                    time2 = now_time - 1

                    path1 = "risk:res:case:dyna_var:completed_approval:daily:project_code:" \
                            "product_code:{}:{}:{}".format(time2, self.project_code, self.product_code)
                    index.append(path1)

                elif flag == 1:
                    if self.before_time != None:
                        time = self.re_time(self.before_time)

                    else:
                        time = now_time
                    path = "risk:res:case:dyna_var:completed_approval:daily:project_code:" \
                           "product_code:{}:{}:{}".format(time, self.project_code, self.product_code)
                    index.append(path)

                else:

                    print("flag只能输入1或0")
            else:
                if flag == 0:
                    time1 = now_time
                    time2 = now_time - 1

                    path1 = "risk:res:case:dyna_var:completed_approval:daily:project_code:" \
                            "product_code:{}:{}:{}:var_inner:{}".format(time2, self.project_code, self.product_code,
                                                                        self.inner_var)
                    path = "risk:res:case:dyna_var:completed_approval:daily:project_code:" \
                            "product_code:{}:{}:{}".format(time2, self.project_code, self.product_code)
                    index.append(path1)
                    index.append(path)

                elif flag == 1:
                    if self.before_time != None:
                        time = self.re_time(self.before_time)

                    else:
                        time = now_time
                    path = "risk:res:case:dyna_var:completed_approval:daily:project_code:" \
                           "product_code:{}:{}:{}:var_inner:{}".format(time, self.project_code, self.product_code,
                                                                       self.inner_var)

                    path1 = "risk:res:case:dyna_var:completed_approval:daily:project_code:" \
                            "product_code:{}:{}:{}".format(time, self.project_code, self.product_code)
                    index.append(path)
                    index.append(path1)

                else:

                    print("flag只能输入1或0")

        return index

    def insert_control_1(self, path:list, number:int, var_name=None):
        param_map = {}
        param_map1 = {}

        for i in range(number):
            projece_c = self.random_param()[0]
            project_n = self.random_param()[1]
            numbers = random.uniform(10, 20)
            value = str(numbers)
            index1 = ""
            index = ""

            if self.inner_var !=None and var_name != None:
                index = projece_c + '@' + project_n + "#" + var_name + '#' + value
                index1 = projece_c + '@' + project_n + '#' + value
            elif var_name == None and self.inner_var==None:
                index = projece_c + '@' + project_n + '#' + value
            else:
                print("输入值有误")

            if self.before_time != None:
                times = self.get_timestamp((datetime.datetime.now() - datetime.timedelta(minutes=self.before_time))
                                           .__format__('%Y-%m-%d %H:%M:%S'))
            else:
                times = int(time.time() * 1000)

            # print(times)

            if index1 != "":
                i_map = {f'{index}': times}  # 利用13位时间戳作为数据的创建时间
                i_map1 = {f'{index1}': times}  # 利用13位时间戳作为数据的创建时间
                param_map.update(i_map)  # 合并字典
                param_map1.update(i_map1)  # 合并字典
            else:
                i_map = {f'{index}': times}  # 利用13位时间戳作为数据的创建时间
                param_map.update(i_map)  # 合并字典

            time.sleep(0.01)

        # print(param_map)

        if len(path) != 1:
            print(self.conn_redis.zadd(name=path[0], mapping=param_map))
            print(self.conn_redis.zadd(name=path[1], mapping=param_map1))

        else:
            print(self.conn_redis.zadd(name=path[0], mapping=param_map))  # 批量插入数据

    def count_sum(self,path, min_time, max_time):
        value_sum = 0
        min_t = self.get_timestamp(min_time)
        max_t = self.get_timestamp(max_time)
        result = self.conn_redis.zrevrangebyscore(name=path, max=max_t, min=min_t)
        for i in result:
            res = str(i, encoding='utf-8').split('#')
            if len(res) == 3:
                value_sum += float(res[2])
            elif res[1] == 'null':
                value_sum += 0
            else:
                value_sum += float(res[1])

        print(round(value_sum, 2))

    def count_sunm1(self, path, minutes=None, days=None, condition=None, operation=None):
        value_sum = 0
        result_s = []
        # max_t = 0
        # min_t = 0
        if minutes != None:
            # max_t = self.get_timestamp(datetime.datetime.now().__format__('%Y-%m-%d %H:%M:%S'))
            #
            # min_t = self.get_timestamp((datetime.datetime.now() - datetime.timedelta(minutes=minutes))
            #                            .__format__('%Y-%m-%d %H:%M:%S'))
            maxs_t = datetime.datetime.now()
            mins_t = (datetime.datetime.now() - datetime.timedelta(minutes=minutes))
            if maxs_t.day == mins_t.day:
                print("等于当天时间")
                max_t = self.get_timestamp(maxs_t.__format__('%Y-%m-%d %H:%M:%S'))
                min_t = self.get_timestamp(mins_t.__format__('%Y-%m-%d %H:%M:%S'))

                result = self.conn_redis.zrevrangebyscore(name=path, max=max_t, min=min_t)

                result_s.append(result)

            else:
                print("不等于当天时间")
                mid_time = '{}-{}-{} 00:00:00'.format(maxs_t.year, maxs_t.month, maxs_t.day)
                mid_time = self.get_timestamp(mid_time)
                max_t = self.get_timestamp(maxs_t.__format__('%Y-%m-%d %H:%M:%S'))
                min_t = self.get_timestamp(mins_t.__format__('%Y-%m-%d %H:%M:%S'))

                today_result = self.conn_redis.zrevrangebyscore(name=path, max=max_t, min=mid_time)

                new_path = self.split_path(path, mins_t, maxs_t)
                yestoday_result = self.conn_redis.zrevrangebyscore(name=new_path, max=mid_time - 1, min=min_t)

                result_s.append(today_result)
                result_s.append(yestoday_result)

        elif days != None:
            print("统计当日累计")
            maxs_t = datetime.datetime.now()
            mid_time = '{}-{}-{} 00:00:00'.format(maxs_t.year, maxs_t.month, maxs_t.day)
            mid_time = self.get_timestamp(mid_time)
            max_t = self.get_timestamp(maxs_t.__format__('%Y-%m-%d %H:%M:%S'))

            result = self.conn_redis.zrevrangebyscore(name=path, max=max_t, min=mid_time)

            result_s.append(result)

        else:
            print("请传值")

        # result = self.conn_redis.zrevrangebyscore(name=path, max=max_t, min=min_t)
        # print(result_s)
        lists = []
        for i in result_s:

            for j in i:

                res = str(j, encoding='utf-8').split('#')

                if len(res) == 3:
                    if operation != None and condition != None:
                        if operation == "=":
                            if res[1] == condition:
                                if res[2] == 'null':
                                    pass

                                else:
                                    value_sum += float(res[2])

                            else:
                                pass
                        elif operation == "contains":
                            cd = condition.split('|')
                            for cds in cd:
                                if cds in res[1]:
                                    if res[2] == 'null':
                                        pass
                                    else:
                                        if j in lists:
                                            break
                                        else:
                                            value_sum += float(res[2])
                                            lists.append(j)

                                else:

                                    pass

                        elif operation == 'in':
                            if res[1] in condition:
                                if res[2] == 'null':
                                    pass
                                else:
                                    value_sum += float(res[2])

                            else:
                                pass

                    elif operation == None and condition != None:
                        cd = condition.split('|')

                        for cds in cd:
                            if cds in res[1]:
                                if res[2] == 'null':
                                    pass
                                else:
                                    if j in lists:
                                        break
                                    else:
                                        value_sum += float(res[2])
                                        lists.append(j)

                            else:
                                pass

                else:
                    if res[1] == 'null':
                        pass
                    else:
                        value_sum += float(res[1])
        # print(lists)
        print(round(value_sum, 2))


if __name__ == '__main__':
    #造数(res规则redis数据)
    date_time = 220111
    # 环境
    env = "test2"
    # condition='A', operation='in'
    # apply_result
    # total_hit_rules
    tc = trendsControl(env=env, project_code='A002', asset_org_no='360JR', inner_var="total_hit_rules", before_time=32)
    #造数
    path = tc.get_path(date_time, flag=1)
    # # print(path)
    excute_result = tc.insert_control_1(path=path, number=3, var_name="C700")
    # # # #
    # # time.sleep(1)
    # # value_sum = ["34.57", "83.68", "49.11"]
    #查询
    # count_path = ["risk:res:case:dyna_var:completed_approval:daily:project_code:asset_org_no:211223:TEST01:360JR:var_inner:total_hit_rules"]
    # for i in count_path:
    #     tc.count_sunm1(path=i, days=1, condition="AC01|AB01")






