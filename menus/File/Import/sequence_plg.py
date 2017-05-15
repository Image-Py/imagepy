# -*- coding: utf-8 -*-
"""
Created on Sat Oct 15 14:42:55 2016
@author: yxl
"""

from imagepy.core.util import fileio
from scipy.misc import imread

class Plugin(fileio.Sequence):
    title = 'Import Sequence'
    filt = ['bmp', 'png', 'jpg', 'gif', 'tif']

    def read(self, path):
        return imread(path)


if __name__ == '__main__':
    print(Plugin.title)
    app = wx.App(False)
    Plugin().run()