# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 00:56:00 2016
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
        ParaDialog.init_view(self, items, para, True)
    
    def para_check(self, para, key):
        if key=='thr1':para['thr2'] = max(para['thr1'], para['thr2'])
        if key=='thr2':para['thr1'] = min(para['thr1'], para['thr2'])
        lim1 = 1.0 * (para['thr1'] - self.lim[0])/(self.lim[1]-self.lim[0])
        lim2 = 1.0 * (para['thr2'] - self.lim[0])/(self.lim[1]-self.lim[0])
        self.histcvs.set_lim(lim1*255, lim2*255)
        self.reset()
        return True
        
class Plugin(Filter):
    title = 'Gray Stairs'
    note = ['all', 'auto_msk', 'auto_snap', 'not_channel', 'preview']
    arange = (0,255)
    #parameter
    

    def load(self, ips):
        if ips.imgtype in ('8-bit', 'rgb'):
            self.para = {'thr1':0, 'thr2':255}
            self.view = [('slide', (0,255), 'Low', 'thr1', ''),
                ('slide', (0,255), 'High', 'thr2', '')]
            if 'not_slice' in self.note:
                self.note.remove('not_slice')
        else :
            self.arange = minv, maxv = ips.img.min(), ips.img.max()
            self.para = {'thr1':ips.range[0], 'thr2':ips.range[1]}
            self.view = [('slide', (minv, maxv), 'Low', 'thr1', ''),
                ('slide', (minv, maxv), 'High', 'thr2', '')]
            if not 'not_slice' in self.note:
                self.note.append('not_slice')
        return True
        
    def show(self):
        self.dialog = ThresholdDialog(IPy.get_window(), self.title)
        hist = np.histogram(self.ips.lookup(),list(range(257)))[0]
        self.dialog.init_view(self.view, self.para, hist, self.arange)
        self.dialog.set_handle(lambda x:self.preview(self.ips, self.para))
        return self.dialog.ShowModal()

    #process
    def run(self, ips, snap, img, para = None):
        if not ips.imgtype in ('8-bit', 'rgb'):
            ips.range = (para['thr1'], para['thr2'])
            return
        img[:] = snap
        np.subtract(img, para['thr1'], out=img, casting='unsafe')
        k = 255.0/max(para['thr2']-para['thr1'], 1)
        np.multiply(img, k, out=img, casting='unsafe')
        img[snap<para['thr1']] = 0
        img[snap>para['thr2']] = 255