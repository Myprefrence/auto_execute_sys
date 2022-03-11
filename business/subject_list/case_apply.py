# -*- coding: utf-8 -*-

# @Time : 2022/3/10 16:48

# @Author : WangJun

# @File : case_apply.py

# @Software: PyCharm
from database.query_subject_case_apply import *
import json
from common.date_encoder import *

class caseApplyMessage:

    def __init__(self, mysql, xn, env):

        self.xn = xn
        self.env = env
        self.mysql = mysql

    def case_apply_message(self, case_apply_no):
        """风控审批信息"""
        case_message = repay(self.mysql, self.xn, self.env).cae_apply(case_apply_no)
        apply_id = case_message['id']
        apply_no = case_message['apply_no']
        order_id = case_message['order_id']
        fb_no = case_message['fb_no']
        asset_org_no = case_message['asset_org_no']
        asset_loan_order_no = case_message['asset_loan_order_no']
        project_no = case_message['project_no']
        project_code = case_message['project_code']
        project_name = case_message['project_name']
        project_version = case_message['project_version']
        product_code = case_message['product_code']
        biz_no = case_message['biz_no']
        user_id = case_message['platform_user_id']
        apply_phone_id = case_message['platform_mobile_id']
        id_type = case_message['id_type']
        id_no = case_message['id_no']
        mobile_no = case_message['mobile_no']
        apply_result = case_message['apply_result']
        result_code = case_message['result_code']
        approve_datetime = case_message['resp_time']
        apply_datetime = case_message['apply_datetime']
        loan_date = case_message['loan_date']
        loan_term = case_message['loan_term']
        irr_rate = case_message['irr_rate']
        loan_amt = case_message['loan_amt']
        asset_credit_amt = case_message['asset_credit_amt']
        asset_used_amt = case_message['asset_used_amt']
        exec_model = case_message['exec_model']
        req_data = case_message['req_data']
        resp_data = case_message['resp_data']
        is_delete = case_message['enable']

        case_strategy_message = repay(self.mysql, self.xn, self.env).case_strategy(apply_id)
        total_hit_rules = case_strategy_message['total_hit_rules']
        approve_chain = case_strategy_message['approve_chain']
        credit_query_success = case_strategy_message['credit_query_success']
        credit_query_fail = case_strategy_message['credit_query_fail']
        test_general_tag = case_strategy_message['test_general_tag']
        asset_level = case_strategy_message['asset_level']
        tq01_result = case_strategy_message['tq01_result']
        general_random = case_strategy_message['general_random']
        output_data = case_strategy_message['output_data']
        output_data_inner = case_strategy_message['output_data_inner']

        case_data = {
            "apply_id": apply_id,
            "apply_no": apply_no,
            "order_id": order_id,
            "asset_loan_order_no": asset_loan_order_no,
            "fb_no": fb_no,
            "asset_org_no": asset_org_no,
            "project_no": project_no,
            "project_code": project_code,
            "project_name": project_name,
            "project_version": project_version,
            "product_code": product_code,
            "id_type": id_type,
            "biz_no": biz_no,
            "user_id": user_id,
            "apply_phone_id": apply_phone_id,
            "id_no": id_no,
            "mobile_no": mobile_no,
            "apply_result": apply_result,
            "result_code": result_code,
            "apply_datetime": apply_datetime,
            "approve_datetime": approve_datetime,
            "loan_date": loan_date,
            "loan_term": loan_term,
            "irr_rate": irr_rate,
            "loan_amt": loan_amt,
            "asset_credit_amt": asset_credit_amt,
            "asset_used_amt": asset_used_amt,
            "exec_model": exec_model,
            "total_hit_rules": total_hit_rules,
            "approve_chain": approve_chain,
            "credit_query_success": credit_query_success,
            "credit_query_fail": credit_query_fail,
            "test_general_tag": test_general_tag,
            "asset_level": asset_level,
            "tq01_result": tq01_result,
            "general_random": general_random,
            "req_data": req_data,
            "output_data": output_data,
            "resp_data": resp_data,
            "output_data_inner": output_data_inner,
            "is_delete": is_delete,

        }
        return json.dumps(case_data, cls=DateEncoder, ensure_ascii=False)
        # return order_data

if __name__ == '__main__':
    # jly是融担环境，mysql=adb，xn=dw时，是查adb库， mysql=rds时，xn=dw时，是查rds库
    mysql = "jly"
    xn = "xna"
    env = "test1"
    apply_no = "XNAB032203100011480616"
    print(caseApplyMessage(mysql, xn, env).case_apply_message(apply_no))


