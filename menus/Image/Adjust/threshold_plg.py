# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 22:56:50 2016
@author: yxl
"""
from imagepy import IPy
import numpy as np
from imagepy.core.engine import Filter
from imagepy.ui.panelconfig import ParaDialog
from imagepy.ui.widgets import HistCanvas

class ThresholdDialog(ParaDialog):
    def init_view(self, items, para, hist):
        self.histcvs = HistCanvas(self)
        self.histcvs.set_hist(hist)
        self.add_ctrl('hist', self.histcvs)
        ParaDialog.init_view(self, items, para, True, False)
    
    def para_check(self, para, key):
        if key=='thr1':para['thr2'] = max(para['thr1'], para['thr2'])
        if key=='thr2':para['thr1'] = min(para['thr1'], para['thr2'])
        self.histcvs.set_lim(para['thr1'], para['thr2'])
        self.reset()
        return True
        
class Plugin(Filter):
    modal = False
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
        
    def cancel(self, ips):
        ips.lut = self.lut
        ips.update = 'pix'
        
    def show(self):
        print('threshold show')
        self.dialog = ThresholdDialog(IPy.get_window(), self.title)
        hist = np.histogram(self.ips.get_img(),list(range(257)))[0]
        self.dialog.init_view(self.view, self.para, (hist*(100.0/hist.max())).astype(np.uint8))
        self.dialog.set_handle(lambda x:self.preview(self.para))
        self.dialog.on_ok = lambda : self.ok(self.ips)
        self.dialog.on_cancel = lambda : self.cancel(self.ips)
        self.dialog.Show()

    def preview(self, para):
        self.ips.lut[:] = self.lut
        self.ips.lut[:para['thr1']] = [0,255,0]
        self.ips.lut[para['thr2']:] = [255,0,0]
        self.ips.update = 'pix'
    
    #process
    def run(self, ips, snap, img, para = None):
        if para == None: para = self.para
        ips.lut = self.lut
        img[:] = 0
        img[snap>=para['thr2']] = 255
        img[snap<para['thr1']] = 255