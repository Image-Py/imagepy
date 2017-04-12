# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 00:56:00 2016

@author: yxl
"""

from core.engines import Filter
from ui.panelconfig import ParaDialog
from ui.widgets import HistCanvas
import IPy
import numpy as np

class ThresholdDialog(ParaDialog):
    def init_view(self, items, para, hist):
        self.histcvs = HistCanvas(self)
        self.histcvs.set_hist(hist)
        self.add_ctrl('hist', self.histcvs)
        ParaDialog.init_view(self, items, para, True)
    
    def para_check(self, para, key):
        mid = 128-para['bright']
        length = 255/np.tan(para['contrast']/180.0*np.pi)
        self.histcvs.set_lim(mid-length/2, mid+length/2)
        self.reset()
        return True
        
class Plugin(Filter):
    title = 'Bright And Constract'
    note = ['all', 'auto_msk', 'auto_snap', 'not_channel', 'preview']
    
    #parameter
    para = {'bright':0, 'contrast':45}
    
    view = [('slide', (-100,100), 'Brightness', 'bright', ''),
            ('slide', (1,89), 'Contrast', 'contrast', '')]
        
    def show(self):
        self.dialog = ThresholdDialog(IPy.get_window(), self.title)
        hist = np.histogram(self.ips.get_img(),range(257))[0]
        self.dialog.init_view(self.view, self.para, (hist*(100.0/hist.max())).astype(np.uint8))
        self.dialog.set_handle(lambda x:self.preview(self.para))
        return self.dialog.ShowModal()

    #process
    def run(self, ips, snap, img, para = None):
        if para == None: para = self.para
        mid = 128-para['bright']
        length = 255/np.tan(para['contrast']/180.0*np.pi)
        print 255/np.tan(para['contrast']/180.0*np.pi)/2
        print mid-length/2, mid+length/2
        img[:] = snap
        if mid-length/2>0:
            np.subtract(img, mid-length/2, out=img, casting='unsafe')
            np.multiply(img, 255.0/length, out=img, casting='unsafe')
        else:
            np.multiply(img, 255.0/length, out=img, casting='unsafe')
            np.subtract(img, (mid-length/2)/length*255, out=img, casting='unsafe')
        img[snap<mid-length/2] = 0
        img[snap>mid+length/2] = 255