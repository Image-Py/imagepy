# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 22:56:50 2016
@author: yxl
"""
from imagepy import IPy
import numpy as np
from imagepy.core.engine import Filter
import scipy.ndimage as ndimg

class Plugin(Filter):
    title = 'Double Threshold'
    note = ['8-bit', 'auto_msk', 'auto_snap', 'preview']
    
    para = {'thr1':255, 'thr2':255}
    view = [('slide', (0,255), 'Low', 'thr1', ''),
                ('slide', (0,255), 'High', 'thr2', '')]

    def load(self, ips):
        self.buflut = ips.lut
        ips.lut = ips.lut.copy()
        return True
    
    def preview(self, ips, para):
        ips.lut[:] = self.buflut
        ips.lut[para['thr2']:] = [0,255,0]
        ips.lut[para['thr1']:] = [255,0,0]
        ips.update = 'pix'

    #process
    def run(self, ips, snap, img, para = None):
        ips.lut = self.buflut
        lab, n = ndimg.label(snap>para['thr2'], np.ones((3,3)), output=np.uint16)
        sta = ndimg.sum(snap>para['thr1'], lab, index=range(n+1)) > 0
        img[:] = (sta*255)[lab]
