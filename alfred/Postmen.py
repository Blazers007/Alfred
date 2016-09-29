#!/usr/bin/env python
#coding=utf-8
import zipfile
import os
import json
import sys
import tempfile
# bcs
from baidupcsapi import PCS
# Dropbox
import dropbox
# Email
import smtplib
from email import Encoders
from email.header import Header
from email.MIMEBase import MIMEBase
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.mime.multipart import MIMEMultipart


BASE_FOLDER='../Warehouse/'


def zipFolder(folder):
    """打包指定的文件夹以及文件夹一级目录内的所有文件

    Args:
        folder: 需要打包的文件夹路径
    """
    # TODO: 出错重新删除并打包
    zf = zipfile.ZipFile('../Mailbox/1.zip', 'w', zipfile.zlib.DEFLATED)
    for img in os.listdir(folder):
        zf.write('../Warehouse/%s' % img, img)
    zf.close()


def _format_addr(s):
    """编码对应的邮件信息

    Args:
        s: 需要编码的字符

    Returns:
        返回对应的Header对象
    """
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))


def sendEmail(fileName, account, password, conf):
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

def sendBCS(fileName, account, password):
    """上传至百度云

    未保存Cookie/Cookie过期的时候会要求输入指定网址提供的验证码

    Args:
        fileName:   上传的文件路径
        account:    百度云账号
        password:   百度云密码
    """
    print('Logging to bcs')
    # TODO: if need to enter the code send an email to me with a form-data url whick i can enter the code
    pcs = PCS(account, password)
    print('Logging successful, Start uploading...')
    chinksize = 1024*1024*2
    fid = 1
    md5list = []
    tmpdir = tempfile.mkdtemp('bdpcs')
    with open(fileName, 'rb') as infile:
        while 1:
            data = infile.read(chinksize)
            if len(data) == 0:
                break
            smallfile = os.path.join(tmpdir, 'tmp%d' % fid)
            with open(smallfile, 'wb') as f:
                f.write(data)
            print 'Uploading chunk%d size %d' % (fid, len(data))
            fid += 1
            ret = pcs.upload_tmpfile(open(smallfile, 'rb'))
            md5list.append(json.loads(ret.content)['md5'])
            os.remove(smallfile)
    os.rmdir(tmpdir)
    ret = pcs.upload_superfile('/Alfred/Whole/%s' % os.path.basename(fileName), md5list)
    print(ret.content)
    print('Uploading Successful')


def sendToDropbox(fileName, token):
    '''发送文件到dropbox
    Args:
        fileName:   发送的文件
        token:      Dropbox的API Token
    '''
    client = dropbox.client.DropboxClient(token)
    print('linked account: ', client.account_info())

    f = open(fileName, 'rb')
    response = client.put_file('/%s' % os.path.basename(fileName), f)
    print('uploaded: ', response)

    folder_metadata = client.metadata('/')
    print('metadata: ', folder_metadata)

    pass

def __test__():
    # 读取JSON文件
    account = json.load(file('../account.json'))
    conf = json.load(file('../config.json'))
    # 打包文件
    zipFolder('../Warehouse/')
    # 上传单个文件至百度云
    # sendBCS('../Mailbox/1.zip', account['bcs']['username'], account['bcs']['password'])
    # 上传文件夹到百度云
    # sendBCSFolder('../Warehouse', account['bcs']['username'], account['bcs']['password'])
    # 发送DropBox
    sendToDropbox('../Mailbox/1.zip', account['dropbox'])
    # 发送邮件提醒
    sendEmail('../Mailbox/1.zip',account['email']['username'],account['email']['password'],conf)


if __name__ == '__main__':
    __test__()
