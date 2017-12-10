# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 22:05:43 2016
@author: yxl
"""
import numpy as np
from scipy.ndimage import label, generate_binary_structure

from imagepy import IPy
from imagepy.core.engine import Filter
from imagepy.imageplus import ImagePlus
from imagepy.ui.canvasframe import CanvasFrame

class Plugin(Filter):
    title = 'Label Image'
    note = ['8-bit', 'not_slice', 'preview']
    
    para = {'thr':128, 'con':'4-Connect'}
    view = [('slide', (0,255), 'Threshold', 'thr', ''),
            (list, ['4-Connect','8-Connect'], str, 'Structure', 'con', 'connect')]
        
    def load(self, ips):
        self.lut = ips.lut
        ips.lut = self.lut.copy()
        return True
        
    def preview(self, ips, para):
        ips.lut[:] = self.lut
        ips.lut[para['thr']:] = [255,0,0]
        ips.update = 'pix'
        
    def run(self, ips, snap, img, para = None):
        if para == None: para = self.para
        ips.lut = self.lut
        msk = img>para['thr']
        con = 1 if para['con']=='4-Connect' else 2
        strc = generate_binary_structure(2, con)
        msk = label(msk, strc, output = np.int16)
        
        IPy.show_img([msk[0]], ips.title+'-label') 
        
        
        