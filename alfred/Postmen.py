#!/usr/bin/env python
#coding:utf-8
import zipfile
import os
from baidupcsapi import PCS
import smtplib
from email import Encoders
from email.header import Header
from email.MIMEBase import MIMEBase
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.mime.multipart import MIMEMultipart

BASE_FOLDER='../Warehouse/'

'''
    打包指定的文件夹以及文件夹一级目录内的所有文件
'''
def zipFolder(folder):
    # TODO: 出错重新删除并打包
    zf = zipfile.ZipFile('../Mailbox/1.zip', 'w', zipfile.zlib.DEFLATED)
    for img in os.listdir(folder):
        zf.write('../Warehouse/%s' % img, img)
    zf.close()

'''
    编码信息
'''
def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))

'''
    发送邮件给自己
'''
def sendEmail(fileName, account, password, smtp, port):
    # 连接并登录邮箱服务器
    # server = smtplib.SMTP_SSL(smtp, port)
    server = smtplib.SMTP(smtp, port)
    server.set_debuglevel(1)
    server.login(account, password)
    # 构造消息
    msg = MIMEMultipart()
    msg['From'] = _format_addr('Alfred <oldgentlemen@gothanm.org>')
    msg['To'] = _format_addr('Old Driver <%s>' % account)
    msg['Subject'] = Header('Today\'s gift', 'utf-8')
    msg.attach(MIMEText('Here is today\'s gift...', 'plain', 'utf-8'))
    # 添加附件
    with open(fileName, 'rb') as f:
        mime = MIMEBase('application', 'octet-stream', fileName='1.zip')
        mime.add_header('Content-Disposition', 'attachment', filename='1.zip')
        mime.add_header('Content-ID', '<0>')
        mime.add_header('X-Attachment-Id', '0')
        # 把附件的内容读进来:
        mime.set_payload(f.read())
        # 用Base64编码:
        Encoders.encode_base64(mime)
        # 添加到MIMEMultipart:
        msg.attach(mime)
    # 发送邮件
    server.sendmail(account, [account], msg.as_string())
    server.quit()
    pass

'''
    上传至百度云
'''
def sendBCS(fileName, account, password):
    print 'Logging to bcs'
    # TODO: if need to enter the code send an email to me with a form-data url whick i can enter the code
    pcs = PCS(account, password)
    print 'Uploading...'
    ret = pcs.upload('/', open(fileName, 'rb').read(), fileName)
    pass

def __test__():
    # 打包文件
    zipFolder('../Warehouse/')
    # 上传至百度云
    # sendBCS('../Mailbox/1.zip', 'username', 'password')
    sendEmail('../Mailbox/1.zip', 'mlmlk007@163.com', 'taaita1314', 'smtp.163.com', 25)
    pass


if __name__ == '__main__':
    __test__()
