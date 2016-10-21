#!/usr/bin/env python
#coding=utf-8
from pymongo import MongoClient
from datetime import datetime
from functools import reduce
from DatabaseManager import STDDataBean
import operator
import requests
# 数据库对象
db = MongoClient().test
collection = db['NGA']

def download(urlList, savingFolder):
    # 遍历文件并下载
    for url in urlList:
        fileType = url.split('.')[-1]
        print('[下载] %s' % url)
        r = requests.get(url, stream=True)
        with open('../Warehouse/1.' + fileType, 'wb') as f:
            for chunk in r.iter_content(10*1024):
                f.write(chunk)
                f.flush()
            f.close()

def retry_when_idle():
    """定时任务: 遍历数据库中下载失败的列表开始下载
    """
    pass

def download(image_bean):
    """开始下载
    """
    # TODO: 若目前有打包任务 则pass等待下一次
    # 超出失败次数则标志放弃任务
    try:
        r = requests.get(self.url, stream=True)
        with open('../Warehouse/1.' + fileType, 'wb') as f:
            for chunk in r.iter_content(10*1024):
                f.write(chunk)
                f.flush()
            f.close()
    except:
        self.retry_times += 1
    finally:
        if self.retry_times > 10:
            # 删除 并处收集信息 已邮件形式发送
            pass

def download_post(std_bean):
    """下载 - 封装文件夹 - 集合打包  每日四次扫描 一次打包发送
        Folder: alfred[打包日期] -----
                                    - [Post_Init_Title] ----
                                                            - Pic1.type
                                                            - Pic2.type
                                                            - Pic3.type
                                                            - content1.html
                                                            - content2.html
                                                            - db.json(DataBase)
                                    - [Post_Init_Title] ----
    """
    # 查找出没有完成的Post对象开始下载 下载到指定文件夹 该文件夹一段时间后被删除(目前设定30天) @ Cleaner.py
    # 查看是否已经有文件夹 没有则创建文件夹
    # 查看更新的页面内容 写 html 文件
    # 覆盖db.json数据库内容
    if not std_bean or not isinstance(std_bean, STDDataBean):
        return
    # Sniffer get base code
    # Create Folder with name
    # List images to download, download and save
    list = std_bean.get_undownload_list()
    # write html file
    # Done


# For testing
def test():
    items = collection.find({'images.download': False}, {'_id': False, 'images': True})
    # 测试 - 查找没有下载的URL
    pics = list(filter(lambda x: not x['download'], reduce(operator.add, list(map(lambda x: x['images'], items)))))
    print(len(pics))
    for pic in pics:
        print('Download? %s \t Url: %s\n' % ('True' if pic['download'] else 'False', pic['url']))
    # 正式使用 需要Title字段作为文件夹名称


if __name__ == '__main__':
    test()
    pass
