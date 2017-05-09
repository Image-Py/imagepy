# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 00:56:00 2016

@author: yxl
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 22:56:50 2016

@author: yxl
"""
from core.engine import Filter
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
        if key=='thr1':para['thr2'] = max(para['thr1'], para['thr2'])
        if key=='thr2':para['thr1'] = min(para['thr1'], para['thr2'])
        self.histcvs.set_lim(para['thr1'], para['thr2'])
        self.reset()
        return True
        
class Plugin(Filter):
    title = 'Gray Stairs'
    note = ['all', 'auto_msk', 'auto_snap', 'not_channel', 'preview']
    
    #parameter
    para = {'thr1':0, 'thr2':255}
    view = [('slide', (0,255), 'Low', 'thr1', ''),
            ('slide', (0,255), 'High', 'thr2', '')]
        
    def show(self):
        self.dialog = ThresholdDialog(IPy.get_window(), self.title)
        hist = np.histogram(self.ips.get_img(),list(range(257)))[0]
        self.dialog.init_view(self.view, self.para, (hist*(100.0/hist.max())).astype(np.uint8))
        self.dialog.set_handle(lambda x:self.preview(self.para))
        return self.dialog.ShowModal()

    #process
    def run(self, ips, snap, img, para = None):
        if para == None: para = self.para
        img[:] = snap
        np.subtract(img, para['thr1'], out=img, casting='unsafe')
        k = 255.0/max(para['thr2']-para['thr1'], 1)
        np.multiply(img, k, out=img, casting='unsafe')
        img[snap<para['thr1']] = 0
        img[snap>para['thr2']] = 255