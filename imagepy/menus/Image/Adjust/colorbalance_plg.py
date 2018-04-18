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

class BalanceDialog(ParaDialog):   
    def para_check(self, para, key):
        mid = 128-para['b_red']
        length = 255/np.tan(para['c_red']/180.0*np.pi)
        self.ctrl_dic['red'].set_lim(mid-length/2, mid+length/2)
        mid = 128-para['b_green']
        length = 255/np.tan(para['c_green']/180.0*np.pi)
        self.ctrl_dic['green'].set_lim(mid-length/2, mid+length/2)
        mid = 128-para['b_blue']
        length = 255/np.tan(para['c_blue']/180.0*np.pi)
        self.ctrl_dic['blue'].set_lim(mid-length/2, mid+length/2)
        #self.reset()
        return True
        
class Plugin(Filter):
    title = 'Color Balance'
    note = ['rgb', 'auto_msk', 'auto_snap', 'not_channel', 'preview']
    
    #parameter
    para = {'b_red':0, 'c_red':45,'b_green':0, 'c_green':45,'b_blue':0, 'c_blue':45}

    def load(self, ips):
        hists = [np.histogram(ips.img[:,:,i],list(range(257)))[0] for i in (0,1,2)]
        self. view = [('hist', 'red', hists[0]),
                      ('slide', 'b_red',   (-100,100), 0, 'Brightness'),
                      ('slide', 'c_red',   (1,89), 0, 'Contrast'),
                      ('hist', 'green', hists[0]),
                      ('slide', 'b_green', (-100,100), 0, 'Brightness'),
                      ('slide', 'c_green', (1,89), 0, 'Contrast'),
                      ('hist', 'blue', hists[2]),
                      ('slide', 'b_blue',  (-100,100), 0, 'Brightness'),
                      ('slide', 'c_blue',  (1,89), 0, 'Contrast')]
        return True
    
    def show(self, temp=BalanceDialog):
        return Filter.show(self, temp)

    #process
    def run(self, ips, snap, img, para = None):
        for i, c in zip([0,1,2],['red','green','blue']):
            mid = 128-para['b_'+c]
            length = 255/np.tan(para['c_'+c]/180.0*np.pi)
            xs = np.linspace(0,255,256)
            ys = 128 + (xs-mid)*(255/length)
            index = np.clip(ys, 0, 255).astype(np.uint8)
            img[:,:,i] = index[snap[:,:,i]]