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
        mid = 128-para['b_red']
        length = 255/np.tan(para['c_red']/180.0*np.pi)
        self.redcvs.set_lim(mid-length/2, mid+length/2)
        mid = 128-para['b_green']
        length = 255/np.tan(para['c_green']/180.0*np.pi)
        self.greencvs.set_lim(mid-length/2, mid+length/2)
        mid = 128-para['b_blue']
        length = 255/np.tan(para['c_blue']/180.0*np.pi)
        self.bluecvs.set_lim(mid-length/2, mid+length/2)
        self.reset()
        return True
        
class Plugin(Filter):
    title = 'Color Balance'
    note = ['all', 'auto_msk', 'auto_snap', 'not_channel', 'preview']
    
    #parameter
    para = {'b_red':0, 'c_red':45,'b_green':0, 'c_green':45,'b_blue':0, 'c_blue':45}
    view = [('slide', (-100,100), 'Brightness', 'b_red', ''),
            ('slide', (1,89), 'Contrast', 'c_red', ''),
            ('slide', (-100,100), 'Brightness', 'b_green', ''),
            ('slide', (1,89), 'Contrast', 'c_green', ''),
            ('slide', (-100,100), 'Brightness', 'b_blue', ''),
            ('slide', (1,89), 'Contrast', 'c_blue', '')]
    
    def show(self):
        self.dialog = Balance_Dialog(IPy.get_window(), self.title)
        self.dialog.init_view(self.para, self.view, self.ips.img)
        self.dialog.set_handle(lambda x:self.preview(self.ips, self.para))
        return self.dialog.ShowModal()

    #process
    def run(self, ips, snap, img, para = None):
        for i, c in zip([0,1,2],['red','green','blue']):
            mid = 128-para['b_'+c]
            length = 255/np.tan(para['c_'+c]/180.0*np.pi)
            img[:,:,i] = snap[:,:,i]
            if mid-length/2>0:
                np.subtract(img[:,:,i], mid-length/2, out=img[:,:,i], casting='unsafe')
                np.multiply(img[:,:,i], 255.0/length, out=img[:,:,i], casting='unsafe')
            else:
                np.multiply(img[:,:,i], 255.0/length, out=img[:,:,i], casting='unsafe')
                np.subtract(img[:,:,i], (mid-length/2)/length*255, out=img[:,:,i], casting='unsafe')
            img[:,:,i][snap[:,:,i]<mid-length/2] = 0
            img[:,:,i][snap[:,:,i]>mid+length/2] = 255