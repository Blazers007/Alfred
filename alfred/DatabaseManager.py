#!/usr/bin/env python
#coding=utf-8
from pymongo import MongoClient
from datetime import datetime

# 数据库对象
db = MongoClient().test
collection = db['NGA']

class STDDataBean(object):
    """数据存储对象的标准结构

    Attributes:
        time:       <string>    Post的时间 - (Unique)
        url:        <string>    对应响应Post/页面的的URL地址 - (Unique)
        author:     <string>    对应的作者名称 - (Unique)
        titles:     <array>     标题,若有修改则append至末端 - (Array Unique)
        contents:   <array>     不同版本的内容,只进不出 - (Array Unique)
        images:     <array>     保存的Image路径数组,有新的则append到末端,只进不出 - (Array Unique)
    """

    @staticmethod
    def parse(datas):
        """从数据库中的结构解析为对象
        """
        if not datas:
            return None
        # 遍历 查找或生成数据对象
        for data in datas:
            if isinstance(data, STDDataBean):
                # 查看数据库中是否已经有数据
                pass

    def __init__(self, url, author, title, content, images, time):
        """初始化STDDataBean对象
        Args:
            =*=注意=*= titles contents images 需要是数组类型
        """
        self.url = url
        self.author = author
        self.titles = set([title])
        self.contents = set([content])
        self.images = images
        self.time = time

    def __insert__(self):
        """只负责初次创建
        """
        obj = {
            "url": self.url,
            "author": self.author,
            "titles": list(self.titles),
            "contents": list(self.contents),
            "images": list(map(lambda x: {'url': x, 'download': False, 'upload': False, 'retry_times': 0}, list(self.images))),
            "time": self.time
        }
        print(collection.insert_one(obj).inserted_id)

    def __update__(self):
        """添加新的image到数组中去 数组必须已经保存过才能正确更新
        Args:
            title:      当前的标题
            content:    当前的内容
            images:     当前的Image数组
        Return:
            返回更新的images数组 需要重新下载
        """
        # 取出数据
        saved = collection.find_one({'url': self.url})
        # 标题整合
        saved_titles = set(saved['titles'])
        addition_titles = self.titles - saved_titles
        # 内容整合
        saved_contents = set(saved['contents'])
        addition_contents = self.contents - saved_contents
        # 图像整合
        saved_images = set(list(map(lambda x: x['url'], saved['images'])))
        addition_images = self.images - saved_images
        # Update all
        _id = collection.update_one({'url': self.url},
            {'$pushAll':{
                'titles': list(addition_titles),
                'contents': list(addition_contents),
                'images': list(map(lambda x: {'url': x, 'download': False, 'upload': False, 'retry_times': 0}, list(addition_images)))
            }}).upserted_id
        print('[Update Successfully]:    Titles: %d\tContents: %d\tImages: %d' % (len(addition_titles), len(addition_contents), len(addition_images)))

    # save
    def save(self):
        """ 保存数据 内部分为update与insert
        """
        if collection.count({'url': self.url}):
            self.__update__()
        else:
            self.__insert__()

def __test__():
    """测试方法
    """
    url = 'scheme://host:port'
    img = 'http://mt1.baidu.com/timg?wh_rate=0&wapiknow&quality=100&size=w250&sec=0&di=3cb34a265801b5bc6e830d82a7e88135&src=http%3A%2F%2Fd.hiphotos.baidu.com%2Fzhidao%2Fwh%253D800%252C450%2Fsign%3D78f6a711ff03918fd78435c2610d0aa3%2F9f510fb30f2442a7c2e20d54d943ad4bd0130256.jpg'
    # Tesing specific forumn name
    for i in range(10):
        a = STDDataBean(url=url+str(i), author='author', title='天青色等烟雨而我在等你', content='天青色等烟雨', images=set([img, '44', '88', '99']), time=datetime.now().strftime('%Y-%m-%d %X'))
        a.save()
        # Update download status
    collection.update_many({'images.url': img}, {'$inc':{'images.$.retry_times': 1}})
    collection.update_many({'images.url': img}, {'$set':{'images.$.upload': True}})
    collection.update_many({'images.url': img}, {'$set':{'images.$.download': True}})
    # print(collection.find_one({'images.url': '8899174'}))

if __name__ == "__main__":
    __test__()
