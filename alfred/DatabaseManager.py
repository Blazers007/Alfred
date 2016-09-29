#!/usr/bin/env python
#coding=utf-8
from pymongo import MongoClient

db = MongoClient().test
collection = db['NGA']

class STDDataBean(object):
    """数据存储对象的标准结构

    Attributes:
        time:       <string>    Post的时间
        url:        <string>    对应响应Post/页面的的URL地址 - (Unique)
        titles:     <array>     标题,若有修改则append至末端 - (Array Unique)
        contents:   <array>     不同版本的内容,只进不出
        images:     <array>     保存的Image路径数组,有新的则append到末端,只进不出
    """

    @staticmethod
    def from_db(bean):
        """从数据库中的结构解析为对象
        """
        return STDDataBean(bean['url'], bean['titles'], bean['contents'], bean['images'], bean['time'], save=False)

    def __init__(self, url, titles, contents, images, time=None, save=True):
        """初始化STDDataBean对象

        默认通过参数构建的对象都会先存储到数据库中去

        Args:
            =*=注意=*= titles contents images 需要是数组类型
        """
        self.url = url
        self.titles = titles
        self.contents = contents
        self.images = set(images)
        if time:
            self.time = time
        else:
            self.time = 1
        # 直接保存
        if save :
            pass


    def _save(self):
        """保存目前的变量到数据库中 insert/update

        Args:
            collection:     Mongodb

        """
        obj = {
            "url": self.url,
            "titles": self.titles,
            "contents": self.contents,
            "images": list(self.images),
            "time": self.time
        }
        _id = collection.insert_one(obj).inserted_id
        return _id

    def compare_and_add_images(self, images):
        """添加新的image到数组中去 数组必须已经保存过才能正确更新
        Args:
            images:  新增的Image数组
        Return:
            返回更新的images数组 需要重新下载
        """
        images = set(images)
        additions = images - self.images
        self.images.update(additions)
        # Update
        _id = collection.update_one({'url': self.url},{'$pushAll':{'images': list(additions)}}).upserted_id
        return additions

def __test__():
    # Tesing specific forumn name
    a = STDDataBean('url', ['title_1'], ['content_1'], ['1', '2', '3'])
    # # Testing method compare_and_add_images
    print(a.images)
    print(a.compare_and_add_images(['3', '4', '5']))
    print(a.images)
    # Testing class method from database
    print('-----Recovery from database-----')
    b = STDDataBean.from_db(collection.find_one({'url': 'url'}))
    print(b.images)
    print(b.compare_and_add_images(['5', '6', '7']))
    print(b.images)
    pass

if __name__ == "__main__":
    __test__()
