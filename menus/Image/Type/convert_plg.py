# -*- coding: utf-8 -*-
"""
Created on Sat Dec 17 14:15:41 2016
@author: yxl
"""
import numpy as np
from imagepy.core.engine import Simple
from imagepy import IPy

class To8bit(Simple):
    title = '8-bit'
    note = ['rgb']

    def run(self, ips, imgs, para = None):
        n = ips.get_nslices()
        if ips.is3d:
            img8 = np.zeros(ips.size+(n,), dtype=np.uint8)
            for i in range(n):
                IPy.curapp.set_progress(round((i+1)*100.0/len(imgs)))
                img8[i] = imgs[i].mean(axis=2)
        else:
            img8 = []
            for i in range(n):
                IPy.set_progress(round((i+1)*100.0/len(imgs)))
                img8.append(imgs[i].mean(axis=2).astype(np.uint8))
        IPy.set_progress(0)
        ips.set_imgs(img8)
        
class ToRGB(Simple):
    title = 'RGB'
    note = ['8-bit']

    def run(self, ips, imgs, para = None):
        n = ips.get_nslices()
        if ips.is3d:
            rgb = np.zeros(ips.size()+(n,), dtype=np.uint8)
            for i in range(n):
                IPy.curapp.set_progress(round((i+1)*100.0/len(imgs)))
                rgb[i] = ips.lut[imgs[i]]
        else:
            rgb = []
            for i in range(n):
                IPy.curapp.set_progress(round((i+1)*100.0/len(imgs)))
                rgb.append(ips.lut[imgs[i]])
        IPy.curapp.set_progress(0)
        ips.set_imgs(rgb)
        
plgs = [To8bit, ToRGB]