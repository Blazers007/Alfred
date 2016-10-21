#!/usr/bin/env python
#coding=utf-8

"""
格式：\033[显示方式;前景色;背景色m

说明：

前景色            背景色           颜色
---------------------------------------
30                40              黑色
31                41              红色
32                42              绿色
33                43              黃色
34                44              蓝色
35                45              紫红色
36                46              青蓝色
37                47              白色

显示方式           意义
-------------------------
0                终端默认设置
1                高亮显示
4                使用下划线
5                闪烁
7                反白显示
8                不可见

例子：
\033[1;31;40m    <!--1-高亮显示 31-前景色红色  40-背景色黑色-->
\033[0m          <!--采用终端默认设置，即取消颜色设置-->
"""

class Logger(object):

    @staticmethod
    def e(msg):
        print('\033[1;37;41m[ERROR]:    ' + msg + '\033[0m')

    @staticmethod
    def ne(msg):
        print('')
        Logger.e(msg)

    @staticmethod
    def i(msg):
        print('\033[1;32;40m[INFO]:    ' + msg + '\033[0m')

    @staticmethod
    def ni(msg):
        print('')
        Logger.i(msg)

    @staticmethod
    def d(msg):
        print('\033[1;32;40m[INFO]:    ' + msg + '\033[0m')


    @staticmethod
    def nd(msg):
        print('')
        Logger.d(msg)

    @staticmethod
    def w(msg):
        print('\033[1;33;41m[INFO]:    ' + msg + '\033[0m')


    @staticmethod
    def nw(msg):
        print('')
        Logger.w(msg)

    @staticmethod
    def a(msg):
        print('\033[1;31;40m[ERROR]:    ' + msg + '\033[0m')

    @staticmethod
    def na(msg):
        print('')
        Logger.a(msg)
