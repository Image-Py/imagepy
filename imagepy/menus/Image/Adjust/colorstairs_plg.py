# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 00:56:00 2016

@author: yxl
"""
import numpy as np
from sciapp.action import Filter
#from imagepy.ui.widgets import HistCanvas
        
class Plugin(Filter):
    title = 'Color Stairs'
    note = ['rgb', 'auto_msk', 'auto_snap', 'not_channel', 'preview']
    para = {'thre_r':(0, 255), 'thre_g':(0, 255), 'thre_b':(0, 255)}

    def load(self, ips):
        hists = [ips.histogram(chans=i, step=512) for i in (0,1,2)]
        self. view = [('hist', 'thre_r', 'lh', hists[0], (0,255), 0),
                      ('hist', 'thre_g', 'lh', hists[1], (0,255), 0),
                      ('hist', 'thre_b', 'lh', hists[2], (0,255), 0)]
        return True

    #process
    def run(self, ips, snap, img, para = None):
        if para == None: para = self.para
        for i, c in zip([0,1,2],'rgb'):
            t1, t2 = para['thre_'+c]
            xs = np.linspace(0,255,256)
            ys = (xs-t1)*(255/max(0.5, t2-t1))
            index = np.clip(ys, 0, 255).astype(np.uint8)
            img[:,:,i] = index[snap[:,:,i]]