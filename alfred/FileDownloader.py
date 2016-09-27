#!/usr/bin/env python
#coding:utf-8
import requests

def download(url):
    fileType = url.split('.')[-1]
    print '[下载] %s' % url
    r = requests.get(url, stream=True)
    with open('../Warehouse/1.' + fileType, 'wb') as f:
        for chunk in r.iter_content(10*1024):
            f.write(chunk)
            f.flush()
        f.close()
