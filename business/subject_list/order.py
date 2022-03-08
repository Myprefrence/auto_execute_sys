# -*- coding: utf-8 -*-

# @Time : 2022/3/8 10:37

# @Author : WangJun

# @File : order.py

# @Software: PyCharm
from database.query_subject_order import *
import json
from common.date_encoder import *

class OrderMessage:

    def __init__(self, mysql, xn, env):

        self.xn = xn
        self.env = env
        self.mysql = mysql

    def order_message(self, asset_loan_order_no):
        order_message = repay(self.mysql, self.xn, self.env).order(asset_loan_order_no)
        order_id = order_message['id']
        order_no = order_message['cap_loan_order_no']
        asset_loan_no = order_message['asset_loan_no']

        order_data = {
            "order_id": order_id,
            "order_no": order_no,
            "order_id": order_id,
        }

        return json.dumps(order_data, cls=DateEncoder, ensure_ascii=False)


if __name__ == '__main__':
    # jly是融担环境，mysql=adb，xn=dw时，是查adb库， mysql=rds时，xn=dw时，是查rds库
    mysql = "jly"
    xn = "xna"
    env = "test2"
    # 身份证号码
    id_no = "110101199609076995"
    asset_loan_order_no = "xVXehmCa1646727500"
    print(OrderMessage(mysql, xn, env).order_message(asset_loan_order_no))
