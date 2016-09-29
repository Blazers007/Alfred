#!/usr/bin/env python
#coding=utf-8
form pymongo import MongoClient

client = mongoClient()

class STDDataBean(object):
    """数据存储对象的标准结构

    Attributes:
        time:       <string>    Post的时间
        url:        <string>    对应响应Post/页面的的URL地址 - (Unique)
        titles:     <array>     标题,若有修改则append至末端 - (Array Unique)
        images:     <array>     保存的Image路径数组,有新的则append到末端,只进不出
        contents:   <array>     不同版本的内容,只进不出
    """

    @staticmethod
    def from_db(**kwargs):
        """从数据库中的结构解析为对象
        """

    def __init__(self, url, titles, images, contents):
        """初始化STDDataBean对象

        Args:
            =*=注意=*= titles images contents 需要是数组类型
        """
        self.url = url
        self.titles = titles
        self.images = images
        self.contents = contents

    def conpare_and_add_images(self, images):
        """添加新的image到数组中去

        Return:
            返回更新的images数组 需要重新下载
        """
        return urls


    def update(self, manager):
        """保存目前的变量到数据库中 insert/update

        Args:
            manager:    Pymongo管理对象

        """
        obj = {
            "tile": self.time,
            "url": self.url,
            "titles": self.titles,
            "images": self.images,
            "contents": self.contents
        }
        # Insert
        manager.insert_one()
        # Update
        pass
