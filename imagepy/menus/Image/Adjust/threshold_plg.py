# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 22:56:50 2016
@author: yxl
"""

import numpy as np
from sciapp.action import Filter

class Plugin(Filter):
    modal = False
    title = 'Threshold'
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
        self.lut = ips.lut
        ips.lut = self.lut.copy()
        return True

    def cancel(self, ips):
        ips.lut = self.lut

    def preview(self, ips, para):
        ips.lut[:] = self.lut
        thr1 = int((para['thre_lh'][0]-self.arange[0])*(
            255.0/max(1e-10, self.arange[1]-self.arange[0])))
        thr2 = int((para['thre_lh'][1]-self.arange[0])*(
            255.0/max(1e-10, self.arange[1]-self.arange[0])))
        # print(thr1, thr2)
        ips.lut[:thr1] = [0,255,0]
        ips.lut[thr2:] = [255,0,0]
    
    def run(self, ips, snap, img, para = None):
        if para == None: para = self.para
        ips.lut = self.lut
        img[:] = 0
        img[snap>=para['thre_lh'][1]] = 255
        img[snap<para['thre_lh'][0]] = 255
        ips.range = (0, 255)