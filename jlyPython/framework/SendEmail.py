# coding:utf-8

import os, sys
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jlyPython.framework import readConfigFile

# reportPath = os.path.dirname(os.path.abspath('.')) + '/testReports/'
reportPath =os.path.abspath(os.curdir)+ '/testReports/'

print("打印路径：")

print(reportPath)
config = readConfigFile.ReadConfig()


class SendMail(object):
    def __init__(self):
        global host, user, password, port, sender, title, content
        host = config.get_email("mail_host")
        user = config.get_email("mail_user")
        password = config.get_email("mail_pass")
        port = config.get_email("mail_port")
        sender = config.get_email("sender")
        title = config.get_email("subject")
        content = config.get_email("content")
        self.value = config.get_email("receiver")
        self.receiver = []
        # get receiver list
        for n in str(self.value).split("/"):
            self.receiver.append(n)


    def get_report(self):  # 该函数的作用是为了在测试报告的路径下找到最新的测试报告

        dirs = os.listdir(reportPath)
        dirs.sort()
        newreportname = dirs[-1]
        print('The new report name: {0}'.format(newreportname))
        return newreportname  # 返回的是测试报告的名字

    def take_messages(self):  # 该函数的目的是为了 准备发送邮件的的消息内容
        newreport = self.get_report()
        self.msg = MIMEMultipart()
        self.msg['Subject'] = title  # 邮件的标题
        self.msg['date'] = time.strftime('%a, %d %b %Y %H:%M:%S %z')

        with open(os.path.join(reportPath, newreport), 'rb') as f:
            mailbody = f.read()  # 读取测试报告的内容
        html = MIMEText(mailbody, _subtype='html', _charset='utf-8')  # 将测试报告的内容放在 邮件的正文当中
        self.msg.attach(html)  # 将html附加在msg里

        # html附件    下面是将测试报告放在附件中发送
        att1 = MIMEText(mailbody, 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'

        att1["Content-Disposition"] = 'attachment; filename="TestReport.html"'  # 这里的filename可以任意写，写什么名字，附件的名字就是什么
        self.msg.attach(att1)

    def send(self):

       # recipients = ['xxxx@xxxx.com', 'xxxx@qq.com', 'xxx@xxxxx.com']  # 发送给多个人
        recipients = ['1605571914@qq.com','yunqing_lei@guochuangmimedia.com'] #发送给一个人
        self.take_messages()
        self.msg['from'] = sender  # 发送邮件的人，这种是公司邮箱转发
        self.msg['to'] =','.join(recipients)   # 收件人和发送人必须这里定义一下，执行才不会报错。
        toaddrs = recipients

        smtp = smtplib.SMTP()
        smtp.connect(host)
        smtp.ehlo()
        smtp.login(user, password)
        smtp.sendmail(self.msg['from'], toaddrs, self.msg.as_string())  # 发送邮件
        smtp.close()
        print('sendmail success')


if __name__ == '__main__':
    sendMail = SendMail()
    sendMail.send()