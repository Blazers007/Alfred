#!/usr/bin/env python
#coding=utf-8
import importlib
import os
import DatabaseManager
import FileDownloader
import Postmen

PLUGIN_PATH = './'
PLUGIN = None

# 遍历所有plugins下面的package

def loadTargetPlugin(pluginName):
    current = list_all_plugins()


# 指定调用的插件名称 / 从 config.json 中读取配置

# 访问插件提供的页面

# 获取HTML内容 -> 生成基本的数据列 POST_ URL

# 与数据库内容对比 更新需要加载的数据列

# 根据数据列 POST _ URL 解析需要下载的图片路径列表

# 下载对应的图片并存放到对应目录

# - Parallel execute -  定时执行ZIP打包与Email/上传网盘任务

def listAllValidPlugins():
    print('加载插件列表\n')
    plugins = []
    for target in os.listdir(PLUGIN_PATH):
        if os.path.isdir(PLUGIN_PATH+target):
            # TODO: 调用测试的Testing方法确保所有需要的方法都拥有!!!
            print('  - 插件:\t%s' % target)
            plugins.append(target)
    print('\n总共插件数量%s' % len(plugins))
    return plugins


'''
    Func 测试用
'''
def __test__():
    # 列出所有可用插件
    plugins = listAllValidPlugins()
    # 选择并加载插件
    PLUGIN=importlib.importmodule('NGA')
    # 首先获取第一页的HTML内容 并返回给 插件解析
    PLUGIN.Translate.
    pass

if __name__ == "__main__":
    __test__()
