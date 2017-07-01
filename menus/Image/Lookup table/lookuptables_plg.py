# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 21:13:42 2016
@author: yxl
"""
from imagepy import IPy
import numpy as np
from imagepy import ImagePlus
from imagepy.ui.canvasframe import CanvasFrame
from imagepy.core.engine import Free
from imagepy.core.manager import ColorManager

class Plugin(Free):
    def __init__(self, key):
        self.title = key
    
    def load(self):
        plus = IPy.get_ips()
        if plus==None:
            img = np.ones((30,1), dtype=np.uint8) * np.arange(256, dtype=np.uint8)
            ips = ImagePlus([img], self.title)
            ips.lut = ColorManager.get_lut(self.title)
            IPy.show_ips(ips)
            return False
        elif plus.channels != 1:
            IPy.alert('RGB image do not surport Lookup table!')
            return False
        return True

    #process
    def run(self, para = None):
        plus = IPy.get_ips()
        plus.lut = ColorManager.get_lut(self.title)
        plus.update = 'pix'
    
    def __call__(self):
        return self
          
plgs = [Plugin(i) for i in list(ColorManager.luts.keys())]
for i in range(len(plgs)):
    if plgs[i].title == 'Grays':
        plgs.insert(0, plgs.pop(i))

if __name__ == '__main__':
    print(list(ColorManager.luts.keys()))
    