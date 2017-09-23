# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 23:43:44 2016
@author: yxl
"""
from imagepy.core.engine import Simple
import numpy as np
from imagepy.core.pixel import bliter
from imagepy import IPy

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

    def run(self, ips, imgs, para = None):
        old = ips.size
        shp = (para['w'], para['h'])
        chns = ips.get_nchannels()
        if chns>1:shp = (shp[1], shp[0], chns)
        
        if para['hor'] == 'left':c=0
        if para['ver'] == 'top':r=0
        if para['hor'] == 'center':c=(shp[1]-old[1])//2
        if para['ver'] == 'center':r=(shp[0]-old[0])//2
        if para['hor'] == 'right':c=shp[1]-old[1]
        if para['ver'] == 'bottom':r=shp[0]-old[0]
            
        if ips.is3d:
            s = list(imgs.shape)
            s[1], s[2] = shp[0], shp[1]
            rst = np.zeros(s, dtype=ips.dtype)
            for i in range(len(imgs)):
                self.progress(i, len(imgs))
                bliter.blit(rst[i], imgs[i], c, r)
        else:
            rst = []
            for i in range(len(imgs)):
                self.progress(i, len(imgs))
                rst.append(np.zeros(shp, ips.dtype))
                bliter.blit(rst[-1], imgs[i], c, r)
        ips.roi = None
        ips.set_imgs(rst)
        if ips.backimg is None: return
        nbc = np.zeros(shp, dtype=np.uint8)
        bliter.blit(nbc, ips.backimg, c, r)
        ips.backimg = nbc

