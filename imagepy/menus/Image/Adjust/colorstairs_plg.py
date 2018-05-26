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

class StairsDialog(ParaDialog): 
        
    def para_check(self, para, key):
        self.ctrl_dic['red'].set_lim(para['t1_red'], para['t2_red'])
        self.ctrl_dic['green'].set_lim(para['t1_green'], para['t2_green'])
        self.ctrl_dic['blue'].set_lim(para['t1_blue'], para['t2_blue'])
        if key == 't1_red':para['t2_red']=max(para['t2_red'], para['t1_red'])
        if key == 't2_red':para['t1_red']=min(para['t2_red'], para['t1_red'])
        if key == 't1_green':para['t2_green']=max(para['t2_green'], para['t1_green'])
        if key == 't2_green':para['t1_green']=min(para['t2_green'], para['t1_green'])
        if key == 't1_blue':para['t2_blue']=max(para['t2_blue'], para['t1_blue'])
        if key == 't2_blue':para['t1_blue']=min(para['t2_blue'], para['t1_blue'])
        self.reset()
        return True
        
class Plugin(Filter):
    title = 'Color Stairs'
    note = ['rgb', 'auto_msk', 'auto_snap', 'not_channel', 'preview']
    
    #parameter
    para = {'t1_red':0, 't2_red':255,'t1_green':0, 't2_green':255,'t1_blue':0, 't2_blue':255}
    def load(self, ips):
        hists = [np.histogram(ips.img[:,:,i],list(range(257)))[0] for i in (0,1,2)]
        self. view = [('hist', 'red', hists[0]),
                      ('slide', 't1_red',   (0,255), 0, 'Low'),
                      ('slide', 't2_red',   (0,255), 0, 'High'),
                      ('hist', 'green', hists[0]),
                      ('slide', 't1_green',   (0,255), 0, 'High'),
                      ('slide', 't2_green', (0,255), 0, 'Low'),
                      ('hist', 'blue', hists[2]),
                      ('slide', 't1_blue',  (0,255), 0, 'Low'),
                      ('slide', 't2_blue',  (0,255), 0, 'High')]
        return True

    def show(self, temp=StairsDialog):
        return Filter.show(self, temp)

    #process
    def run(self, ips, snap, img, para = None):
        if para == None: para = self.para
        for i, c in zip([0,1,2],['red','green','blue']):
            t1, t2 = para['t1_'+c], para['t2_'+c]
            xs = np.linspace(0,255,256)
            ys = (xs-t1)*(255/max(0.5, t2-t1))
            index = np.clip(ys, 0, 255).astype(np.uint8)
            img[:,:,i] = index[snap[:,:,i]]