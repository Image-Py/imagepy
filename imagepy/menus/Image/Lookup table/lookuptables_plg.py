# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 21:13:42 2016
@author: yxl
"""
from imagepy import root_dir
import numpy as np
#from imagepy.core import ImagePlus
from sciapp.action import Free
from imagepy.app import ColorManager
from sciapp.object import Image

class LUT(Free):
    def __init__(self, key, v):
        self.title, self.lut = key, v

    def run(self, para = None):
        ips = self.app.get_img()
        if ips==None:
            img = np.arange(256*30, dtype=np.uint8).reshape((-1,256))
            ips = Image([img], self.title)
            ips.lut = self.lut
            return self.app.show_img(ips)
        if ips.channels != 1:
            return self.app.alert('only one channel image surport Lookup table!')
        ips.lut = self.lut
        ips.update()
    
    def __call__(self): return self
          
plgs = [LUT(i, j) for i, j, _ in ColorManager.gets(tag='base')]
    