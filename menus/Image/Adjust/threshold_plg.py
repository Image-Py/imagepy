# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 22:56:50 2016

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
        print hist
        self.add_ctrl('hist', self.histcvs)
        ParaDialog.init_view(self, items, para, True)
    
    def para_check(self, para, key):
        if key=='thr1':para['thr2'] = max(para['thr1'], para['thr2'])
        if key=='thr2':para['thr1'] = min(para['thr1'], para['thr2'])
        self.histcvs.set_lim(para['thr1'], para['thr2'])
        self.reset()
        return True
        
class Plugin(Filter):
    title = 'Threshold'
    note = ['all', 'auto_msk', 'auto_snap','preview']
    
    #parameter
    para = {'thr1':0, 'thr2':255}
    view = [('slide', (0,255), 'Low', 'thr1', ''),
            ('slide', (0,255), 'High', 'thr2', '')]
    
    def load(self, ips):
        self.lut = ips.lut
        ips.lut = self.lut.copy()
        return True
        
    def show(self):
        self.dialog = ThresholdDialog(IPy.get_window(), self.title)
        hist = np.histogram(self.ips.get_img(),range(257))[0]
        self.dialog.init_view(self.view, self.para, (hist*(100.0/hist.max())).astype(np.uint8))
        self.dialog.set_handle(lambda x:self.preview(self.para))
        return self.dialog.ShowModal()

    def preview(self, para):
        self.ips.lut[:] = self.lut
        self.ips.lut[:para['thr1']] = [0,255,0]
        self.ips.lut[para['thr2']:] = [255,0,0]
        self.ips.update = True
    
    #process
    def run(self, ips, img, buf, para = None):
        if para == None: para = self.para
        ips.lut = self.lut
        buf[:] = 0
        buf[img>=para['thr2']] = 255
        buf[img<para['thr1']] = 255