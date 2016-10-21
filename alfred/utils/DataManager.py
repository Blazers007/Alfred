#!/usr/bin/env python
#coding=utf-8
import sys
sys.path.append("..")
from models.PostBeans import STDPostBean

class DataManager(object):

    def get_all_post_list():
        """返回全部PostBeans
        """
        return list(STDPostBean.get_all())
