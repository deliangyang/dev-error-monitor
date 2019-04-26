# -*-- coding:utf-8 -*--
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from config import *


class MailSender:

    __slots__ = ('subject', 'content', 'mail_from', 'mail_to')

    def __init__(self, subject, content, mail_from, mail_to):
        self.subject = subject
        self.content = content
        self.mail_from = mail_from
        self.mail_to = mail_to

    def parse_message(self):
        message = MIMEText(self.content, 'plain', 'utf-8')
        message['Subject'] = self.subject
        message['From'] = formataddr([self.mail_from, self.mail_from])
        message['To'] = duanhaisheng_cc
        message['Cc'] = ','.join([longhaibin_cc, chenqiang_cc, mujianhong_cc, ydl_cc])
        return message

    def send(self):
        server = smtplib.SMTP_SSL(mail_host, 465)
        server.login(user_name, password)
        return server.sendmail(
            self.mail_from,
            self.mail_to,
            self.parse_message().as_string()
        )
