# -*- coding: utf-8 -*-
"""
Created on Sat Oct 15 14:42:55 2016
@author: yxl
"""

from imagepy.core.util import fileio
from scipy.misc import imread
from imagepy.core.manager import OpenerManager

class Plugin(fileio.Sequence):
    title = 'Import Sequence'
    
    def load(self):
        self.filt = sorted(OpenerManager.all())
        return True

if __name__ == '__main__':
    print(Plugin.title)
    app = wx.App(False)
    Plugin().run()