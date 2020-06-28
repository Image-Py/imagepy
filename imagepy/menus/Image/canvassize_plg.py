# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 23:43:44 2016
@author: yxl
"""
from sciapp.action import Simple
import numpy as np

def make_slice(a, b, mode=1):
    aa, bb = sorted([a, b])
    if mode == 0: sb = slice(0, aa)
    if mode == 1: sb = slice((bb-aa)//2, (bb-aa)//2+aa)
    if mode == 2: sb = slice(bb-aa, bb)
    return (slice(None), sb)[::(-1,1)[a<b]]

class Plugin(Simple):
    title = 'Canvas Size'
    note = ['all']
    
    para = {'w':0, 'h':0, 'hor':'center', 'ver':'center'}
    view = [(int, 'w', (1,2048), 0, 'Weight', 'pix'),
            (int, 'h', (1,2048), 0, 'Height', 'pix'),
            (list, 'hor', ['left', 'center', 'right'], str, 'Horizontal', ''),
            (list, 'ver', ['top', 'center', 'bottom'], str, 'Vertical', '')]
            
    def load(self, ips):
        self.para['h'], self.para['w'] = ips.shape
        return True

    def run(self, ips, imgs, para = None):
        (o_r, o_c), n, n_r, n_c = ips.shape, ips.channels, para['h'], para['w']
        key = {'left':0, 'center':1, 'right':2, 'top':0, 'bottom':1}
        or_sli, nr_sli = make_slice(o_r, n_r, key[para['ver']])
        oc_sli, nc_sli = make_slice(o_c, n_c, key[para['hor']])
        shp = (ips.slices, n_r, n_c, ips.channels)[:3+(ips.channels>1)]
        if ips.isarray: buf = np.zeros(shp, dtype=ips.dtype)
        else: buf = [np.zeros(shp[1:], dtype=ips.dtype) for i in range(shp[0])]

        for i in range(ips.slices):
            self.progress(i, ips.slices)
            buf[i][nr_sli, nc_sli] = imgs[i][or_sli, oc_sli]
        ips.set_imgs(buf)