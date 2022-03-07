# -*- coding: utf-8 -*-

# @Time : 2022/3/3 19:43

# @Author : WangJun

# @File : send_email.py

# @Software: PyCharm


from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

"""
SMTP是发送邮件的协议，Python内置对SMTP的支持，可以发送纯文本邮件、HTML邮件以及带附件的邮件。

Python对SMTP支持有smtplib和email两个模块，email负责构造邮件，smtplib负责发送邮件。
"""


