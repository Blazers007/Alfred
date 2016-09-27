#!/usr/bin/env python
#coding:utf-8
import zipfile
import os
from baidupcsapi import PCS

BASE_FOLDER='../Warehouse/'

def zipFolder(folder):
    # TODO: 出错重新删除并打包
    zf = zipfile.ZipFile('../Mailbox/1.zip', 'w', zipfile.zlib.DEFLATED)
    for img in os.listdir(folder):
        zf.write('../Warehouse/%s' % img, img)
    zf.close()

def sendEmail(fileName, emailAddress):
    pass

def sendBCS(fileName, account, pwd):
    print 'Logging to bcs'
    # TODO: if need to enter the code send an email to me with a form-data url whick i can enter the code
    pcs = PCS(account, pwd)
    print 'Uploading...'
    ret = pcs.upload('/', open(fileName, 'rb').read(), fileName)
    pass

def __test__():
    zipFolder('../Warehouse/')
    sendBCS('../Mailbox/1.zip', 'username', 'password')


if __name__ == '__main__':
    __test__()
