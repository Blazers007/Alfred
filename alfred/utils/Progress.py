#!/usr/bin/env python
#coding=utf-8
import time
import sys

class ProgressBar(object):
    """进度条

    Attributes:
        current         <int>       当前进度
        total           <int>       总共进度
        show_as_percent <boolean>   前面的字符是否采用百分制显示

    """
    def __init__(self, current, total, show_as_percent=True):
        self.current = current
        self.total = total
        self.show_as_percent = show_as_percent

    def show_progress(self):
        """显示进度 <打印>
        """
        progress = int(self.current / self.total * 100)
        if self.show_as_percent:
            sys.stdout.write('{0:3}/{1:3}: '.format(progress, 100))
        else:
            width = len(str(self.total))
            w1 = '{0:%d}' % width
            w2 = '{1:%d}' % width
            sys.stdout.write(('%s/%s: ' % (w1, w2)).format(self.current, self.total))
        sys.stdout.write('[%s%s]\r' % ('#' * progress, '.' * (100 - progress)))
        sys.stdout.flush()

    def finished(self):
        """进度条是否已经完成
        """
        return self.current >= self.total

    def increase(self, increasement=1, auto_show_progress=True):
        self.current += increasement
        if auto_show_progress:
            self.show_progress()

    @staticmethod
    def sample():
        """静态方法 测试用
        """
        p = ProgressBar(0, 23)
        p.show_progress()
        while not p.finished():
            p.increase()
            time.sleep(0.1)


if __name__ == '__main__':
    """ Just for testing
    """
    p = ProgressBar(0, 23)
    p.show_progress()
    while not p.finished():
        p.increase()
        time.sleep(0.1)
