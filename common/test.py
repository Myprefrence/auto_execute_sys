# -*- coding: utf-8 -*-

# @Time : 2022/2/21 15:52

# @Author :Administrator

# @File : HTTP.py

# @Software: PyCharm
# @Desc:http请求：post,get
#导入pymysql模块
# import pymysql
#
# # 建立连接
# # 连接需要ip（host），端口（port）,用户名（user），密码（password），以及指定是哪个库（db）,指定编码格式（charset，数据库中指定编码格式是utf8！）
# conn=pymysql.connect(
#     host='172.16.11.92',
#     port=3306,
#     user='root',
#     password='HRdXK3TelK6bgGyg',
#     db='dev_prs',
#     charset='utf8'
# )
#
# #拿到游标（游标是给mysql提交命令时的一种接口，个人理解：光标停留的地方，在这个地方你就可以输入sql语句啦）
# cursor=conn.cursor()
#
# #执行sql语句
# # 增、删、改
# # sql= "update t_loan_info_1 set create_datetime='2021-03-01 11:35:36' where asset_loan_order_no='orderNo202109241048569804';"
# sql= "update dev_prs.t_loan_info_1 set cust_age=21 where asset_loan_order_no='orderNo202109241048569804';"
# #对于增删改这种数据变动性操作，必须执行以下提交操作才能真的对数据进行变更
# cursor.execute(sql)
# conn.commit()
#
#  # sql="SELECT * FROM t_loan_info_1 WHERE asset_loan_order_no='orderNo202109241048569804';"
#
#   #交给游标进行查询
#
# # 关闭游标对象
# cursor.close()
# conn.close()

for i in range(10+1):
    print(i)