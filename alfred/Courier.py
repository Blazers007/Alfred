#!/usr/bin/env python
#coding=utf-8
import zipfile
import os
import json
import sys
# Dropbox
import dropbox

BASE_FOLDER='../Warehouse/'


def _zipFolder(folder):
    """打包指定的文件夹以及文件夹一级目录内的所有文件
    Args:
        folder: 需要打包的文件夹路径
    """
    # TODO: 出错重新删除并打包
    zf = zipfile.ZipFile('../Mailbox/1.zip', 'w', zipfile.zlib.DEFLATED)
    for img in os.listdir(folder):
        zf.write('../Warehouse/%s' % img, img)
    zf.close()

def _sendToDropbox(fileName, token):
    """发送文件到dropbox
    Args:
        fileName:   发送的文件
        token:      Dropbox的API Token
    """
    client = dropbox.client.DropboxClient(token)
    print('linked account: ', client.account_info())

    f = open(fileName, 'rb')
    response = client.put_file('/%s' % os.path.basename(fileName), f)
    print('uploaded: ', response)

    folder_metadata = client.metadata('/')
    print('metadata: ', folder_metadata)
    pass

def do_the_job():
    """定时任务/外部可调用方法: 如果当前没有其他任务则占用文件系统开始打包
    """

def __test__():
    # 读取JSON文件
    with open('../account.json', 'r') as f:
        try:
            account = json.load(f)
        except Exception as e:
            print(e)
            account = None
    with open('../config.json', 'r') as f:
        try:
            conf = json.load(f)
        except Exception as e:
            print(e)
            conf = None
    if account and conf:
        print('Loading config successful')
        # 打包文件
        # zipFolder('../Warehouse/')
        # 发送DropBox
        sendToDropbox('../Mailbox/1.zip', account['dropbox'])
    else:
        print('Error: You should spicific the right config in the root volumn')

if __name__ == '__main__':
    __test__()
