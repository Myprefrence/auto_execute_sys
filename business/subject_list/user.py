# -*- coding: utf-8 -*-

# @Time : 2022/3/1 15:22

# @Author : WangJun

# @File : user.py

# @Software: PyCharm

import datetime
import json

from database.query_subject_user import *
import hashlib
from common.parse_idNo import *
from common.date_encoder import *


class UserMessage(object):

    def __init__(self, mysql, xn, env):

        self.xn = xn
        self.env = env
        self.mysql = mysql

    def md5_encryption(self, value):
        md5 = hashlib.md5()
        md5.update(value.encode('utf-8'))
        return md5.hexdigest()

    def sha256_md5_encryption(self, value):
        sha256 = hashlib.sha256()
        sha256.update(value.encode('utf-8'))
        return sha256.hexdigest()

    def get_user_message(self, idNo):
        ceryType = {
            "ID": "1",
            "PASSPORT": "2",
            "统一社会信用代码": "3",
            "OTHERS": "4",
            "证件号缺失": "0",
        }
        certification_type = {
            "实名": "1",
            "未实名": "0",
            "未知": "-1",
        }

        gender_type = {
             1: "M",
             2: "F"
        }

        use_message = repay(self.mysql, self.xn, self.env).eam_message(idNo)
        user_id = use_message['id_no_platform_id']
        apply_phone_id = use_message['mobile_no_platform_id']
        cery_type = "ID"
        id_no_1 = use_message['id_no']
        id_no = f'{id_no_1[: 14]}**{id_no_1[16]}*'
        mobile_no_1 = use_message['mobile_no']
        if ceryType.get(cery_type) == "1":
            cert_no = id_no
        else:
            print("身份证类型不等于1")
            cert_no = id_no
        mobile_no = f'{mobile_no_1[:7]}****'
        cust_name = use_message['cust_name']
        cust_no = use_message['cust_no']
        id_no_md5 = self.md5_encryption(id_no_1)
        mobile_no_md5 = self.md5_encryption(mobile_no_1)
        cust_name_md5 =self.md5_encryption(cust_name)
        id_no_sha256 = self.sha256_md5_encryption(id_no_1)
        mobile_no_sha256 = self.sha256_md5_encryption(mobile_no_1)
        cust_name_sha256 = self.sha256_md5_encryption(cust_name)
        cbs_idNo_message = repay(self.mysql, self.xn, self.env).cbs_idNo_message(idNo)
        is_certification = cbs_idNo_message['replace(JSON_EXTRACT(ext_json, \'$.idCert\'), \'"\',\'\')']
        if is_certification == "Y":
            isCertification = "实名"
        elif is_certification == "N":
            isCertification = "未实名"
        else:
            isCertification = "未知"
        certificate_date_1 = cbs_idNo_message['create_datetime']
        certificate_date = datetime.datetime.strftime(certificate_date_1, '%Y-%m-%d')

        global bank_card_no, bank_code,bank_name,bank_phone
        try:
            cust_info_message = repay(self.mysql, self.xn, self.env).cust_info_message(idNo)
            bank_card_no_1 = cust_info_message['acct']
            bank_card_no = f'{bank_card_no_1[:6]}**********'
            bank_code = cust_info_message['bank_code']
            bank_name = cust_info_message['bank_name']
            bank_phone_1 = cust_info_message['bank_phone']
            bank_phone = f'{bank_phone_1[:7]}****'
        except Exception as e:
            print("调用用户表返回失败和无值，message：%s" % e)

        nation = use_message['cust_nation']
        id_issue_date_1 = str(use_message['id_issue_date'])
        id_issue_date = "{}-{}-{}".format(id_issue_date_1[0:4], id_issue_date_1[4:6], id_issue_date_1[6:])
        id_address = use_message['id_address']
        id_expire_date_1 = str(use_message['id_expire_date'])
        id_expire_date = "{}-{}-{}".format(id_expire_date_1[0:4], id_expire_date_1[4:6], id_expire_date_1[6:])
        id_parse = GetInformation(id_no_1)
        age = id_parse.get_age()
        gender = id_parse.get_sex()
        birth_date = id_parse.get_birthday()

        data = {
            "user_id": user_id,
            "apply_phone_id": apply_phone_id,
            "cert_type": ceryType.get(cery_type),
            "cert_no": cert_no,
            "id_no": id_no,
            "mobile_no": mobile_no,
            "cust_name": cust_name,
            "cust_no": cust_no,
            "id_no_md5": id_no_md5,
            "mobile_no_md5": mobile_no_md5,
            "cust_name_md5": cust_name_md5,
            "id_no_sha256": id_no_sha256,
            "mobile_no_sha256": mobile_no_sha256,
            "cust_name_sha256": cust_name_sha256,
            "is_certification": certification_type.get(isCertification),
            "certificate_date": certificate_date,
            "bank_card_no": bank_card_no,
            "bank_code": bank_code,
            "bank_name": bank_name,
            "bank_phone": bank_phone,
            "age": age,
            "birth_date": birth_date,
            "gender": gender_type.get(gender),
            "nation": nation,
            "id_address": id_address,
            "id_issue_date": id_issue_date,
            "id_expire_date": id_expire_date,
        }

        return json.dumps(data, cls=DateEncoder, ensure_ascii=False)


if __name__ == '__main__':
    # jly是融担环境，mysql=adb，xn=dw时，是查adb库， mysql=rds时，xn=dw时，是查rds库
    mysql = "jly"
    xn = "xna"
    env = "test1"
    # 身份证号码
    id_no = "110101199609076995"
    print(UserMessage(mysql, xn, env).get_user_message(id_no))







