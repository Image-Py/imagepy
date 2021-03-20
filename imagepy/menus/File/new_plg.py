# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 02:38:04 2016

@author: yxl
"""
from sciapp.action import Free
import numpy as np

class Plugin(Free):
    title = 'New Image'
    para = {'name':'Undefined','width':300, 'height':300, 'type':'8-bit','slice':1}
    view = [(str, 'name', 'name', ''),
            (int, 'width',  (1,10240), 0,  'width', 'pix'),
            (int, 'height', (1,10240), 0,  'height', 'pix'),
            (list, 'type', ['8-bit','RGB'], str, 'type', ''),
            (int, 'slice',  (1,2048), 0,  'slice', '')]

    #process
    def run(self, para = None):
        w, h = para['width'], para['height']
        channels = (1,3)[para['type']=='RGB']
        slices = para['slice']
        shape = (h,w,channels) if channels!=1 else (h,w)
        imgs = [np.zeros(shape, dtype=np.uint8) for i in range(slices)]
        self.app.show_img(imgs, para['name'])

if __name__ == '__main__':
    print(Plugin.title)
    app = wx.App(False)
    Plugin().run()