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
    def init_view(self, items, para, hist, lim):
        self.histcvs = HistCanvas(self)
        self.histcvs.set_hist(hist)
        self.lim = lim
        self.add_ctrl('hist', self.histcvs)
        ParaDialog.init_view(self, items, para, True, False)
    
    def para_check(self, para, key):
        if key=='thr1':para['thr2'] = max(para['thr1'], para['thr2'])
        if key=='thr2':para['thr1'] = min(para['thr1'], para['thr2'])
        lim1 = 1.0 * (para['thr1'] - self.lim[0])/(self.lim[1]-self.lim[0])
        lim2 = 1.0 * (para['thr2'] - self.lim[0])/(self.lim[1]-self.lim[0])
        self.histcvs.set_lim(lim1*255, lim2*255)
        self.reset()
        return True
        
class Plugin(Filter):
    modal = False
    title = 'Threshold'
    note = ['all', 'auto_msk', 'auto_snap', 'not_channel', 'preview']
    arange = (0,255)
    
    def load(self, ips):
        if ips.imgtype == '8-bit':
            self.para = {'thr1':0, 'thr2':255}
            self.view = [('slide', (0,255), 'Low', 'thr1', ''),
                ('slide', (0,255), 'High', 'thr2', '')]
        else :
            self.para = {'thr1':ips.range[0], 'thr2':ips.range[1]}
            self.view = [('slide', ips.range, 'Low', 'thr1', ''),
                ('slide', ips.range, 'High', 'thr2', '')]
            self.arange = ips.range
        self.lut = ips.lut
        ips.lut = self.lut.copy()
        return True
        
    def cancel(self, ips):
        ips.lut = self.lut
        ips.update = 'pix'
        
    def show(self):
        print('threshold show')
        self.dialog = ThresholdDialog(IPy.get_window(), self.title)
        hist = np.histogram(self.ips.lookup(),list(range(257)))[0]
        self.dialog.init_view(self.view, self.para, hist, self.ips.range)
        self.dialog.set_handle(lambda x:self.preview(self.ips, self.para))
        self.dialog.on_ok = lambda : self.ok(self.ips)
        self.dialog.on_cancel = lambda : self.cancel(self.ips)
        self.dialog.Show()

    def preview(self, ips, para):
        ips.lut[:] = self.lut
        thr1 = int((para['thr1']-self.arange[0])*(
            255.0/max(1, self.arange[1]-self.arange[0])))
        thr2 = int((para['thr2']-self.arange[0])*(
            255.0/max(1, self.arange[1]-self.arange[0])))
        # print(thr1, thr2)
        ips.lut[:thr1] = [0,255,0]
        ips.lut[thr2:] = [255,0,0]
        ips.update = 'pix'
    
    #process
    def run(self, ips, snap, img, para = None):
        if para == None: para = self.para
        ips.lut = self.lut
        img[:] = 0
        img[snap>=para['thr2']] = 255
        img[snap<para['thr1']] = 255
        ips.range = (0, 255)