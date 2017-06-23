# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 02:38:04 2016

@author: yxl
"""

import wx,os
from imagepy import ImagePlus
from imagepy.ui.canvasframe import CanvasFrame
import numpy as np
from imagepy import IPy

from imagepy.core.engine import Free

class Plugin(Free):
    title = 'New'
    para = {'name':'Undefined','width':300, 'height':300, 'type':'8-bit','slice':1}
    view = [(str, 'name', 'name',''),
            (int, (1,2048), 0,  'width', 'width', 'pix'),
            (int, (1,2048), 0,  'height', 'height', 'pix'),
            (list, ['8-bit','RGB'], str, 'Type', 'type',''),
            (int, (1,2048), 0,  'slice', 'slice', '')]

    #process
    def run(self, para = None):
        w, h = para['width'], para['height']
        channels = (1,3)[para['type']=='RGB']
        slices = para['slice']
        shape = (h,w,channels) if channels!=1 else (h,w)
        imgs = [np.zeros(shape, dtype=np.uint8) for i in range(slices)]
        IPy.show_img(imgs, para['name'])

if __name__ == '__main__':
    print(Plugin.title)
    app = wx.App(False)
    Plugin().run()