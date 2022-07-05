import time
# -*- coding:utf-8 -*-

import pymysql,json,random
from pymysql.constants import CLIENT
# 连接数据库
con = pymysql.connect(host="172.16.11.92", user="root", \
                      password="HRdXK3TelK6bgGyg",\
                      # db="fresho2o",\
                      charset="utf8",\
                      cursorclass=pymysql.cursors.DictCursor,\
                      client_flag=CLIENT.MULTI_STATEMENTS)

class RenH_sql(object):
    def __init__(self,xn,env,project_no,api_no):
        self.xn = xn
        self.env = env
        self.project_no = project_no
        self.api_no = api_no
        self.cur = con.cursor()
    # 1.在disconf/pb_front中配置人行的项目，send.cbs.project.nos=1002,zzx-caxs-xxxx,1001,test111,test222
    # 2.bbs.t_cust_auth_result表，配置对应的项目数据
    def inset_bbs(self,user_id,name):
        sixnum = (int)((random.random() * 9 + 1) * 100000)
        self.cur.execute("select * from `%s_%s_bbs`.t_cust_auth_result where cust_no = '%s';"%(self.xn,self.env,user_id))
        i
        self.cur.execute("INSERT INTO `%s_%s_bbs`.t_cust_auth_result\
        (`id`, `project_no`, `project_name`, `cust_no`, `asset_org_no`, `source_id_no`, `name`, `sex`, `nation`, `birthday`, `address`, `id_no`, `id_sign_group`, `term_start`, `term_end`, `path_sfz_face`, `path_sfz_back`, `auth_book_version`, `be_auth_peoper`, `auth_book_term_start`, `auth_book_term_end`, `path_auth_file`, `ocr_id_no_check_result`, `ocr_id_no_check_result_desc`, `ocr_id_no_term_check_result`, `ocr_id_no_term_check_result_desc`, `face_check_result`, `face_check_result_desc`, `face_confidence`, `path_face_file`, `auth_book_activate_check_result`, `auth_book_activate_check_result_desc`, `id_no_face_check_date`, `id_no_back_check_date`, `auth_book_check_date`, `face_check_date`, `remark`, `create_datetime`, `update_datetime`, `created_by`, `updated_by`)\
         VALUES ('XNAB202204201546450001%s', '%s', NULL, '%s', '360JR', '450802199907181219', '%s', '女', NULL, NULL, NULL, NULL, NULL, NULL, NULL, '/bizdata/xna/businessdata/bbs/back/hf-hw-bxyh/20220421/front_of_id_card.png', '/bizdata/xna/businessdata/bbs/back/hf-hw-bxyh/20220421/reverse_side_of_id_card.png', 'v1', '福建永鸿兴融资担保有限公司', '2021-05-03', '2099-12-31', '/bizdata/xna/businessdata/bbs/back/hf-hw-bxyh/20220421/05.pdf', 'SUCCESS', '通过', 'SUCCESS', '通过', 'SUCCESS', 'NULL', '97.256', '/bizdata/xna/businessdata/bbs/back/hf-hw-bxyh/20220421/人像.png', 'ACTIVE', 'NULL', '2022-04-20 16:03:55', '2022-04-20 15:59:50', '2022-04-20 15:59:46', '2022-04-20 15:47:32', NULL, '2022-04-20 15:46:45', '2022-06-21 15:50:00', 'sys', 'sys');\
        "%(self.xn,self.env,sixnum,self.project_no,user_id,name))
        con.commit()
        print('新增bbs对应项目配置成功')
    # 3.pb-front.t_convert_rule_conf表，设置对应的脱敏方式配置
    def inset_pbfront(self):
        num1 = (int)((random.random() * 9 + 1) * 1000000)
        num2 = (int)((random.random() * 9 + 1) * 1000000)
        num3 = (int)((random.random() * 9 + 1) * 1000000)
        num4 = (int)((random.random() * 9 + 1) * 1000000)
        num5 = (int)((random.random() * 9 + 1) * 1000000)
        self.cur = con.cursor()
        self.cur.execute("select * from `%s_%s_pb-front`.t_convert_rule_conf where project_no = '%s' and api_no = '%s';"%(self.xn,self.env,self.project_no,self.api_no))
        cuu = self.cur.fetchall()
        if not cuu:
            self.cur.execute("INSERT INTO `%s_%s_pb-front`.`t_convert_rule_conf`(`id`, `api_no`, `project_no`, `rule_code`, `rule_name`, `version_code`, `enable`, `create_datetime`, `create_by`, `update_datetime`, `update_by`)\
                                    VALUES ('XNA%s', '%s', '%s', 'original|compress', '原始版', 'original', 'N', NULL, NULL, NULL, NULL);\
                                    " % (self.xn, self.env, num1, self.api_no, self.project_no))
            self.cur.execute("INSERT INTO `%s_%s_pb-front`.`t_convert_rule_conf`(`id`, `api_no`, `project_no`, `rule_code`, `rule_name`, `version_code`, `enable`, `create_datetime`, `create_by`, `update_datetime`, `update_by`) \
                                    VALUES ('XNA%s', '%s', '%s', 'base-masking', '基础脱敏版', 'base-mask', 'Y', NULL, NULL, NULL, NULL);\
                                    " % (self.xn, self.env, num2, self.api_no, self.project_no))
            self.cur.execute("INSERT INTO `%s_%s_pb-front`.`t_convert_rule_conf`(`id`, `api_no`, `project_no`, `rule_code`, `rule_name`, `version_code`, `enable`, `create_datetime`, `create_by`, `update_datetime`, `update_by`)\
                                    VALUES ('XNA%s', '%s', '%s', 'outer-masking', '外部脱敏', 'out-mask', 'N', '2022-04-13 17:31:29', '3', '2022-04-13 17:31:36', '3');\
                                    " % (self.xn, self.env, num3, self.api_no, self.project_no))
            self.cur.execute("INSERT INTO `%s_%s_pb-front`.`t_convert_rule_conf`(`id`, `api_no`, `project_no`, `rule_code`, `rule_name`, `version_code`, `enable`, `create_datetime`, `create_by`, `update_datetime`, `update_by`)\
                                    VALUES ('XNA%s', '%s', '%s', 'outer-masking|compress|encryption', '加密', 'encryption', 'Y', NULL, NULL, NULL, NULL);\
                                    " % (self.xn, self.env, num4, self.api_no, self.project_no))
            self.cur.execute("INSERT INTO `%s_%s_pb-front`.`t_convert_rule_conf`(`id`, `api_no`, `project_no`, `rule_code`, `rule_name`, `version_code`, `enable`, `create_datetime`, `create_by`, `update_datetime`, `update_by`)\
                                    VALUES ('XNA%s', '%s', '%s', 'standard', '标准版', 'standard', 'N', NULL, NULL, NULL, NULL);\
                                    " % (self.xn, self.env, num5, self.api_no, self.project_no))
            con.commit()
            print('为空，pb-front.t_convert_rule_conf脱敏配置成功')
        else:

            i = set(['原始版','外部脱敏','基础脱敏版','标准版','加密'])
            l = []
            for j in cuu:
                l.append(j["rule_name"])
            l1 = set(l)
            i1 = i-l1
            for c in i1:
                if c == "原始版":
                    self.cur.execute("INSERT INTO `%s_%s_pb-front`.`t_convert_rule_conf`(`id`, `api_no`, `project_no`, `rule_code`, `rule_name`, `version_code`, `enable`, `create_datetime`, `create_by`, `update_datetime`, `update_by`)\
                                                                VALUES ('XNA%s', '%s', '%s', 'original|compress', '原始版', 'original', 'N', NULL, NULL, NULL, NULL);\
                                                                " % (
                    self.xn, self.env, num1, self.api_no, self.project_no))
                elif c == "基础脱敏版":
                    self.cur.execute("INSERT INTO `%s_%s_pb-front`.`t_convert_rule_conf`(`id`, `api_no`, `project_no`, `rule_code`, `rule_name`, `version_code`, `enable`, `create_datetime`, `create_by`, `update_datetime`, `update_by`) \
                                                VALUES ('XNA%s', '%s', '%s', 'base-masking', '基础脱敏版', 'base-mask', 'Y', NULL, NULL, NULL, NULL);\
                                                " % (self.xn, self.env, num2, self.api_no, self.project_no))
                elif c == "外部脱敏":
                    self.cur.execute("INSERT INTO `%s_%s_pb-front`.`t_convert_rule_conf`(`id`, `api_no`, `project_no`, `rule_code`, `rule_name`, `version_code`, `enable`, `create_datetime`, `create_by`, `update_datetime`, `update_by`)\
                                                VALUES ('XNA%s', '%s', '%s', 'outer-masking', '外部脱敏', 'out-mask', 'N', '2022-04-13 17:31:29', '3', '2022-04-13 17:31:36', '3');\
                                                " % (self.xn, self.env, num3, self.api_no, self.project_no))
                elif c == "加密":
                    self.cur.execute("INSERT INTO `%s_%s_pb-front`.`t_convert_rule_conf`(`id`, `api_no`, `project_no`, `rule_code`, `rule_name`, `version_code`, `enable`, `create_datetime`, `create_by`, `update_datetime`, `update_by`)\
                                                VALUES ('XNA%s', '%s', '%s', 'outer-masking|compress|encryption', '加密', 'encryption', 'Y', NULL, NULL, NULL, NULL);\
                                                " % (self.xn, self.env, num4, self.api_no, self.project_no))
                elif c == "标准版":
                    self.cur.execute("INSERT INTO `%s_%s_pb-front`.`t_convert_rule_conf`(`id`, `api_no`, `project_no`, `rule_code`, `rule_name`, `version_code`, `enable`, `create_datetime`, `create_by`, `update_datetime`, `update_by`)\
                                                VALUES ('XNA%s', '%s', '%s', 'standard', '标准版', 'standard', 'N', NULL, NULL, NULL, NULL);\
                                                " % (self.xn, self.env, num5, self.api_no, self.project_no))
                con.commit()
                print('缺少%s数据,添加成功'%c)
    # 4.检查是否配置了人行的五个步骤
    def inspect(self):
        self.cur.execute("select * from `%s_%s_pb-front`.t_flow_conf;"%(self.xn,self.env))
        resut = self.cur.fetchall()
        for i in resut:
            if i["step_name"] == '实名认证':
                print("已配置：",i["step_name"])
            elif i["step_name"] == '上传文件':
                print("已配置：", i["step_name"])
            elif i["step_name"] == '查询文件状态':
                print("已配置：", i["step_name"])
            elif i["step_name"] == '报告查询':
                print("已配置：", i["step_name"])
            elif i["step_name"] == '报告结果':
                print("已配置：", i["step_name"])
            else:
                print('请手动检查数据库配置')
                print(i)

    #5.PCY1还需要检验配置
    def PCY1(self):
        seven_num = (int)((random.random() * 9 + 1) * 1000000)
        self.cur.execute("INSERT INTO `%s_ecw`.`t_check_condition_conf`(`id`, `api_no`, `project_no`, `id_no_ocr`, `id_no_valid`, `license_period`, `license_usable`, `warrant_person`, `face`, `create_datetime`, `update_datetime`, `create_by`, `update_by`)\
            VALUES ('%s', 'PCY1', '%s', 'Y', 'Y', 'Y', 'Y', '福建永鸿兴融资担保有限公司', 'Y', '2022-04-18 10:13:20', '2022-05-10 17:35:06', NULL, NULL);\
            "%(self.env,seven_num,self.project_no))
        con.commit()
        print('PCY1的校验插入成功')
if __name__ == '__main__':
    xn = "xna"
    env = "test1"
    project_no = "test222"
    user_id = "CI2206300001450023"
    name = "飞六升"
    """PB01,PB02,PCY"""
    api_no = "PCY"
    basic = RenH_sql(xn,env,project_no,api_no)
    basic.inset_bbs(user_id,name)
    # basic.inset_pbfront()
    # basic.inspect()
    # basic.PCY1()

