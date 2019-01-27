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
from ....core.manager import WindowsManager

class ThresholdDialog(ParaDialog):
    def __init__(self, parent, title, lim):
        ParaDialog.__init__(self, parent, title)
        self.lim = lim

    def para_check(self, para, key):
        if key=='thr1':para['thr2'] = max(para['thr1'], para['thr2'])
        if key=='thr2':para['thr1'] = min(para['thr1'], para['thr2'])
        lim1 = 1.0 * (para['thr1'] - self.lim[0])/(self.lim[1]-self.lim[0])
        lim2 = 1.0 * (para['thr2'] - self.lim[0])/(self.lim[1]-self.lim[0])
        self.ctrl_dic['hist'].set_lim(lim1*255, lim2*255)
        self.reset()
        return True
        
class Plugin(Filter):
    modal = False
    title = 'Threshold'
    note = ['all', 'auto_msk', 'auto_snap', 'not_channel', 'preview']
    arange = (0,255)
    
    def load(self, ips):
        hist = np.histogram(self.ips.lookup(),list(range(257)))[0]
        if ips.imgtype == '8-bit':
            self.para = {'thr1':0, 'thr2':255}
            self.view = [('hist', 'hist', hist),
                         ('slide', 'thr1', (0,255), 0, 'Low'),
                         ('slide', 'thr2', (0,255), 0, 'High')]
        else :
            self.para = {'thr1':ips.range[0], 'thr2':ips.range[1]}
            self.view = [('hist', 'hist', hist,),
                         ('slide', 'thr1', ips.range, 10, 'Low'),
                         ('slide', 'thr2', ips.range, 10, 'High')]
            self.arange = ips.range
        self.lut = ips.lut
        ips.lut = self.lut.copy()
        return True

    def show(self, temp=ThresholdDialog):
        dialog = lambda win, title, lim = self.ips.range:temp(win, title, lim)
        return Filter.show(self, dialog)

    def cancel(self, ips):
        ips.lut = self.lut
        ips.update()

    def preview(self, ips, para):
        ips.lut[:] = self.lut
        thr1 = int((para['thr1']-self.arange[0])*(
            255.0/max(1e-10, self.arange[1]-self.arange[0])))
        thr2 = int((para['thr2']-self.arange[0])*(
            255.0/max(1e-10, self.arange[1]-self.arange[0])))
        # print(thr1, thr2)
        ips.lut[:thr1] = [0,255,0]
        ips.lut[thr2:] = [255,0,0]
        ips.update()
    
    #process
    def run(self, ips, snap, img, para = None):
        if para == None: para = self.para
        ips.lut = self.lut
        img[:] = 0
        img[snap>=para['thr2']] = 255
        img[snap<para['thr1']] = 255
        ips.range = (0, 255)