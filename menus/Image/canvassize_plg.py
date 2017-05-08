# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 23:43:44 2016

@author: yxl
"""

from core.engine import Simple
import numpy as np
from core.pixcel import bliter
import IPy

class Plugin(Simple):
    title = 'Canvas Size'
    note = ['all']
    
    para = {'w':0, 'h':0, 'hor':'center', 'ver':'center'}
    view = [(int, (1,2048), 0, 'Weight', 'w', 'pix'),
            (int, (1,2048), 0, 'Height', 'h', 'pix'),
            (list, ['left', 'center', 'right'], str, 'Horizontal', 'hor', ''),
            (list, ['top', 'center', 'bottom'], str, 'Vertical', 'ver', '')]
            
    def load(self, ips):
        sp = ips.size
        self.para['w'] = sp[1]
        self.para['h'] = sp[0]
        return True

    #process
    def run(self, ips, imgs, para = None):
        old = ips.size
        shp = (para['w'], para['h'])
        chns = ips.get_nchannels()
        if chns>1:shp = (shp[1], shp[0], chns)
        
        if para['hor'] == 'left':c=0
        if para['ver'] == 'top':r=0
        if para['hor'] == 'center':c=(shp[1]-old[1])/2
        if para['ver'] == 'center':r=(shp[0]-old[0])/2
        if para['hor'] == 'right':c=shp[1]-old[1]
        if para['ver'] == 'bottom':r=shp[0]-old[0]
            
        if ips.is3d:
            s = list(imgs.shape)
            s[1], s[2] = shp[0], shp[1]
            rst = np.zeros(s, dtype=ips.dtype)
            for i in range(len(imgs)):
                IPy.curapp.set_progress(round(i*100.0/len(imgs)))
                bliter.blit(rst[i], imgs[i], c, r)
        else:
            rst = []
            for i in range(len(imgs)):
                IPy.curapp.set_progress(round(i*100.0/len(imgs)))
                rst.append(np.zeros(shp, ips.dtype))
                bliter.blit(rst[-1], imgs[i], c, r)
        IPy.curapp.set_progress(0)
        ips.roi = None
        ips.set_imgs(rst)