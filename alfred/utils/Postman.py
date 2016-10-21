#!/usr/bin/env python
#coding=utf-8
import smtplib
from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.mime.multipart import MIMEMultipart

# 发送邮件用
def _format_addr(s):
    """编码对应的邮件信息

    Args:
        s: 需要编码的字符

    Returns:
        返回对应的Header对象
    """
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def _sendEmail(fileName, account, password, conf):
    """发送邮件

    Args:
        fileName:   附件文件() - 发送较大的附件需要一次性占用过多内存，造成在VPS上的python直接killed
        account:    账户名
        password:   密码
        conf:       {'SMTP': 'smtp.qq.com',
                     'SMTPPort': 465,
                     'SSL': True,
                     'sendTo': '308802880@qq.com'}
    """
    # 连接并登录邮箱服务器
    if conf['SSL']:
        server = smtplib.SMTP_SSL(conf['SMTP'], conf['SMTPPort'])
    else:
        server = smtplib.SMTP(conf['SMTP'], conf['SMTPPort'])
    server.set_debuglevel(1)
    server.login(account, password)
    # 构造消息
    msg = MIMEMultipart()
    msg['From'] = _format_addr('Alfred <oldgentlemen@gothanm.org>')
    msg['To'] = _format_addr('Old Driver <%s>' % account)
    msg['Subject'] = Header('Today\'s gift', 'utf-8')
    msg.attach(MIMEText('Here is today\'s gift...', 'plain', 'utf-8'))
    # 添加附件
    # with open(fileName, 'rb') as f:
    #     mime = MIMEBase('application', 'octet-stream', fileName='1.zip')
    #     mime.add_header('Content-Disposition', 'attachment', filename='1.zip')
    #     mime.add_header('Content-ID', '<0>')
    #     mime.add_header('X-Attachment-Id', '0')
    #     # 把附件的内容读进来:
    #     mime.set_payload(f.read())
    #     # 用Base64编码:
    #     Encoders.encode_base64(mime)
    #     # 添加到MIMEMultipart:
    #     msg.attach(mime)
    # 发送邮件
    server.sendmail(account, [conf['sendTo']], msg.as_string())
    server.quit()
