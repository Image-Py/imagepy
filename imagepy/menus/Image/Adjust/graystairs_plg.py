# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 00:56:00 2016
@author: yxl
"""
import numpy as np
from sciapp.action import Filter

        
class Plugin(Filter):
    title = 'Gray Stairs'
    note = ['all', 'auto_msk', 'auto_snap', 'not_channel', 'preview']
    arange = (0,255)

    def load(self, ips):
        hist = ips.histogram(chans='all', step=512)
        if ips.dtype == np.uint8:
            self.para = {'thre_lh':(0, 255)}
            self.view = [('hist', 'thre_lh', 'lh', hist, (0,255), 0)]
        else :
            self.para = {'thre_lh':(ips.range[0], ips.range[1])}
            self.view = [('hist', 'thre_lh', 'lh', hist, ips.range, 10)]
            self.arange = ips.range
            #if not 'not_slice' in self.note:
            #    self.note.append('not_slice')
        return True

    #process
    def run(self, ips, snap, img, para = None):
        if ips.dtype != np.uint8:
            ips.range = para['thre_lh']
            return
        img[:] = snap
        np.subtract(img, para['thre_lh'][0], out=img, casting='unsafe')
        k = 255.0/max(para['thre_lh'][1]-para['thre_lh'][0], 1e-10)
        np.multiply(img, k, out=img, casting='unsafe')
        img[snap<para['thre_lh'][0]] = 0
        img[snap>para['thre_lh'][1]] = 255