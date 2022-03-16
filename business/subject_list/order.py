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

    def order_message(self, asset_loan_order_no, apply_no):
        order_message = repay(self.mysql, self.xn, self.env).order(asset_loan_order_no)

        order_id = order_message['id']
        order_no = order_message['cap_loan_order_no']
        # 订单期数
        loan_period = order_message['loan_period']
        asset_loan_no = order_message['asset_loan_no']
        asset_loan_order_no = order_message['asset_loan_order_no']
        cap_loan_order_no = order_message['cap_loan_order_no']
        asset_org_name = order_message['asset_org_name']
        project_no = order_message['project_no']
        bis_type_id = order_message['bis_type_id']
        bis_type_name = order_message['bis_type_name']
        loan_apply_datetime = order_message['loan_apply_datetime']
        asset_credit_amount = order_message['creditAmt']
        res_message = repay(self.mysql, self.xn, self.env).res(apply_no)
        if asset_credit_amount is None:
            asset_credit_amount = res_message['asset_credit_amount']
            return asset_credit_amount
        asset_used_amount = order_message['usedAmt']
        if asset_used_amount is None:
            asset_used_amount = res_message['asset_used_amount']
            return asset_used_amount
        loan_amt = order_message['loan_amt']
        channel = order_message['channel']
        order_status = order_message['order_status']
        risk_result_desc = order_message['result_code']
        withdraw_datetime = order_message['cap_interest_day']
        withdraw_interest_day = order_message['cap_loan_datetime']
        fee_rate = order_message['annual_rate']
        contract_no = order_message['asset_loan_order_no']
        repay_type = order_message['rpy_type']
        cert_no = order_message['id_no']
        cust_mobile_no = order_message['cust_mobile_no']
        bank_acct_name = order_message['acct_name']
        cust_name = order_message['cust_name']
        bank_code = order_message['bank_code']
        bank_name = order_message['bank_name']
        bank_acct_no = order_message['acct']
        bank_mobile_no = order_message['bank_phone']
        ext_json = order_message['ext_json']
        cust_no = order_message['cust_no']
        user_message = repay(self.mysql, self.xn, self.env).eam_cust_info(cert_no)
        user_id = user_message['id_no_platform_id']
        asser_user_message = repay(self.mysql, self.xn, self.env).eam_assert_cust(cust_no)
        asset_cust_no = asser_user_message["asset_cust_no"]
        apply_phone_id = asser_user_message['mobile_no_platform_id']

        cap_message = repay(self.mysql, self.xn, self.env).cap(order_id)
        aps_meassge = repay(self.mysql, self.xn, self.env).aps(project_no)
        cap_code = cap_message['cap_code']
        remark = cap_message['remark']
        cap_fee_rate = cap_message['loan_rate']
        project_type = aps_meassge['project_type']
        grace_days = cap_message['grace_days']
        if cap_code is None:
            cap_code = aps_meassge['cap_code_json']
            return cap_code
        cap_name = cap_message['cap_name']
        # 订单应收担保费收入
        total_premium = repay(self.mysql, self.xn, self.env).cbs_guarantee_fee(order_id)['订单应收担保费收入']
        # 订单已收担保费收入
        actual_premium = repay(self.mysql, self.xn, self.env).cbs_paid_guarantee(order_id)['订单已收担保费收入']
        # 已还本金
        repay_principal = repay(self.mysql, self.xn, self.env).cbs_rpy_principal(order_id)['已还本金']
        if repay_principal is None:
            repay_principal = 0
        # 最近一次还款时间
        rpy_datetime = repay(self.mysql, self.xn, self.env).cbs_rpy_principal(order_id)['最近一次还款时间']

        if repay_principal >= loan_amt:
            # 订单未还本金
            cur_left_principal = 0
            # 订单结清时间
            order_settle_datetime = rpy_datetime
        else:
            cur_left_principal = loan_amt - repay_principal
            order_settle_datetime = ''

        cbs_rpy_principal_message = repay(self.mysql, self.xn, self.env).cbs_rpy_datetime(order_id)
        # 订单历史最大逾期天数
        max_overdue_days = cbs_rpy_principal_message['订单历史最大逾期天数']
        # 订单当前逾期天数
        cur_overdue_days = cbs_rpy_principal_message['订单当前逾期天数']

        cap_compensatory_message = repay(self.mysql, self.xn, self.env).cap_compensatory(cap_loan_order_no)
        # 累计代偿金额
        total_comp_amount = cap_compensatory_message['累计代偿金额']
        # 累计代偿本金
        total_comp_principal = cap_compensatory_message['累计代偿本金']
        # 累计代偿利息
        total_comp_interest = cap_compensatory_message['累计代偿利息']
        # 累计代偿罚息
        total_comp_od_fee = cap_compensatory_message['累计代偿罚息']

        order_data = {
            "order_id": order_id,
            "order_no": order_no,
            "asset_loan_no": asset_loan_no,
            "asset_loan_order_no": asset_loan_order_no,
            "cap_loan_order_no": cap_loan_order_no,
            "asset_org_name": asset_org_name,
            "project_no": project_no,
            "cap_code": cap_code,
            "cap_name": cap_name,
            "bis_type_id": bis_type_id,
            "bis_type_name": bis_type_name,
            "loan_period": loan_period,
            "asset_credit_amount": asset_credit_amount,
            "loan_amt": loan_amt,
            "asset_used_amount": asset_used_amount,
            "loan_apply_datetime": loan_apply_datetime,
            "channel": channel,
            "order_status": order_status,
            "risk_result_desc": risk_result_desc,
            "cert_no": cert_no,
            "cust_no": cust_no,
            "withdraw_datetime": withdraw_datetime,
            "withdraw_interest_day": withdraw_interest_day,
            "fee_rate": fee_rate,
            "contract_no": contract_no,
            "repay_type": repay_type,
            "user_id": user_id,
            "asset_cust_no": asset_cust_no,
            "apply_phone_id": apply_phone_id,
            "cap_fee_rate": cap_fee_rate,
            "project_type": project_type,
            "grace_days": grace_days,
            "cust_mobile_no": cust_mobile_no,
            "cust_name": cust_name,
            "bank_acct_name": bank_acct_name,
            "bank_code": bank_code,
            "bank_name": bank_name,
            "bank_acct_no": bank_acct_no,
            "bank_mobile_no": bank_mobile_no,
            "ext_json": ext_json,
            "remark": remark,
            "total_premium": total_premium,
            "actual_premium": actual_premium,
            "repay_principal": repay_principal,
            "order_settle_datetime": order_settle_datetime,
            "max_overdue_days": max_overdue_days,
            "cur_overdue_days": cur_overdue_days,
            "total_comp_amount": total_comp_amount,
            "total_comp_principal": total_comp_principal,
            "total_comp_interest": total_comp_interest,
            "total_comp_od_fee": total_comp_od_fee,
            "cur_left_principal": cur_left_principal,

        }

        return json.dumps(order_data, cls=DateEncoder, ensure_ascii=False)
        # return order_data


if __name__ == '__main__':
    # jly是融担环境，mysql=adb，xn=dw时，是查adb库， mysql=rds时，xn=dw时，是查rds库
    mysql = "jly"
    xn = "xna"
    env = "test1"
    # 身份证号码
    id_no = "110101199609076995"
    asset_loan_order_no = "t9D0xnAQ1647415947"
    apply_no = "XNAB032203160011560013"
    print(OrderMessage(mysql, xn, env).order_message(asset_loan_order_no, apply_no))
