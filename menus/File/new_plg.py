# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 02:38:04 2016

@author: yxl
"""

import wx,os
from imageplus import ImagePlus
from ui.canvasframe import CanvasFrame
import numpy as np
import IPy

from core.engine import Free

class Plugin(Free):
    '''
    Creat a new image.
    
    @author: yxdragon
    @e-main: imagepy@sina.com
    '''
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
        chanels = (1,3)[para['type']=='RGB']
        slices = para['slice']
        shape = (h,w,chanels) if chanels!=1 else (h,w)
        imgs = [np.zeros(shape, dtype=np.uint8) for i in range(slices)]
        IPy.show_img(imgs, para['name'])

if __name__ == '__main__':
	print(Plugin.title)
	app = wx.App(False)
	Plugin().run()