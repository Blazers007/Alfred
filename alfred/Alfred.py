#!/usr/bin/env python
#coding=utf-8
import Sniffer
import Courier
import Cleaner
import Server
from utils.Logger import Logger
import sys

# -------------------------- Task1 <Sniffer> ------------------------------------
_sniffer = ['sniffer', 's']
# -------------------------- Task2 <Courier> ------------------------------------
_courier = ['courier', 'cr']
# -------------------------- Task3 <Cleaner> ------------------------------------
_cleaner = ['cleaner', 'cl']



if __name__ == "__main__":
    # 判断task类型
    #Server.run()
    # sys.argv[0] == 脚本名称
    if len(sys.argv) > 1:
        # 开始判断
        arg = sys.argv[1]
        if arg in _sniffer:
            if len(sys.argv) == 3:
                Logger.i('==== [Task]: Sniffer ====\n')
                Sniffer.sniffer(sys.argv[2])
                Logger.ni('==== [Task Done]: Sniffer ====')
            else:
                Logger.e("请输入嗅探的URL地址")
        elif arg in _courier:
            Logger.i('==== [Task]: Courier ====')
            Logger.ni('==== [Task Done]: Courier ====')
        elif arg in _cleaner:
            Logger.i('==== [Task]: Cleaner ====')
            Logger.ni('==== [Task Done]: Cleaner ====')
        else:
            print("参数错误")
    else:
        print("没有提供运行参数")
