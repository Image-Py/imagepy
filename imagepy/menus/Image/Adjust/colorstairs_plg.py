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

class Balance_Dialog(ParaDialog):
    def init_view(self, para, view, img):
        hists = [np.histogram(img[:,:,i],list(range(257)))[0] for i in (0,1,2)]
        self.redcvs = HistCanvas(self)
        self.redcvs.set_hist(hists[0])
        self.greencvs = HistCanvas(self)
        self.greencvs.set_hist(hists[1])
        self.bluecvs = HistCanvas(self)
        self.bluecvs.set_hist(hists[2])
        
        self.add_ctrl('red', self.redcvs)
        self.parse(view[0])
        self.parse(view[1])
        self.add_ctrl('green', self.greencvs)
        self.parse(view[2])
        self.parse(view[3])
        self.add_ctrl('blue', self.bluecvs)
        self.parse(view[4])
        self.parse(view[5])
        
        self.add_check('Preview', 'preview')
        self.add_confirm(True)
        self.reset(para)
        self.pack()
        
    def para_check(self, para, key):
        self.redcvs.set_lim(para['t1_red'], para['t2_red'])
        self.greencvs.set_lim(para['t1_green'], para['t2_green'])
        self.bluecvs.set_lim(para['t1_blue'], para['t2_blue'])
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
    note = ['all', 'auto_msk', 'auto_snap', 'not_channel', 'preview']
    
    #parameter
    para = {'t1_red':0, 't2_red':255,'t1_green':0, 't2_green':255,'t1_blue':0, 't2_blue':255}
    view = [('slide', (0,255), 'Low', 't1_red', ''),
            ('slide', (0,255), 'High', 't2_red', ''),
            ('slide', (0,255), 'Low', 't1_green', ''),
            ('slide', (0,255), 'High', 't2_green', ''),
            ('slide', (0,255), 'Low', 't1_blue', ''),
            ('slide', (0,255), 'High', 't2_blue', '')]
    def show(self):
        self.dialog = Balance_Dialog(IPy.get_window(), self.title)
        self.dialog.init_view(self.para, self.view, self.ips.img)
        self.dialog.set_handle(lambda x:self.preview(self.ips, self.para))
        return self.dialog.ShowModal()

    #process
    def run(self, ips, snap, img, para = None):
        if para == None: para = self.para
        for i, c in zip([0,1,2],['red','green','blue']):
            img[:,:,i] = snap[:,:,i]
            np.subtract(img[:,:,i], para['t1_'+c], out=img[:,:,i], casting='unsafe')
            k = 255.0/max(para['t2_'+c]-para['t1_'+c], 1)
            np.multiply(img[:,:,i], k, out=img[:,:,i], casting='unsafe')
            img[:,:,i][snap[:,:,i]<para['t1_'+c]] = 0
            img[:,:,i][snap[:,:,i]>para['t2_'+c]] = 255