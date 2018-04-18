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
    def __init__(self, parent, title, lim):
        ParaDialog.__init__(self, parent, title)
        self.lim = lim
    
    def para_check(self, para, key):
        mid = 128-para['bright']/(self.lim[1]-self.lim[0])*255
        length = 255/np.tan(para['contrast']/180.0*np.pi)
        self.ctrl_dic['hist'].set_lim(mid-length/2, mid+length/2)
        return True
        
class Plugin(Filter):
    title = 'Bright And Constract'
    note = ['all', 'auto_msk', 'auto_snap', 'not_channel', 'preview']
        
    def load(self, ips):
        hist = np.histogram(self.ips.lookup(),list(range(257)))[0]
        if ips.imgtype in ('8-bit', 'rgb'):
            self.arange = (0, 255)
            self.para = {'bright':0, 'contrast':45}
            self.view = [('hist', 'hist', hist),
                         ('slide', 'bright', (-100,100), 0, 'Brightness'),
                         ('slide', 'contrast', (1,89), 0, 'Contrast')]
            if 'not_slice' in self.note:
                self.note.remove('not_slice')
        else :
            self.arange = minv, maxv = ips.img.min(), ips.img.max()
            self.para = {'bright':np.mean(ips.range) - np.mean(self.arange), 
                'contrast':round(np.arctan((maxv-minv)/(ips.range[1]-ips.range[0]))/np.pi*180)}
            self.view = [('hist', 'hist', hist),
                         ('slide', 'bright', (-(maxv-minv)/2, (maxv-minv)/2), 10, 'Brightness'),
                         ('slide', 'contrast', (1,89), 0, 'Contrast')]
            if not 'not_slice' in self.note:
                self.note.append('not_slice')
        return True

    def show(self, temp=ThresholdDialog):
        dialog = lambda win, title, lim = self.ips.range:temp(win, title, lim)
        return Filter.show(self, dialog)


    #process
    def run(self, ips, snap, img, para = None):
        if not ips.imgtype in ('8-bit', 'rgb'):
            mid = (self.arange[0] + self.arange[1])/2 - para['bright']
            length = (self.arange[1] - self.arange[0])/np.tan(para['contrast']/180.0*np.pi)
            ips.range = (mid-length/2, mid+length/2)
            return
        if para == None: para = self.para
        mid = 128-para['bright']
        length = 255/np.tan(para['contrast']/180.0*np.pi)
        print(255/np.tan(para['contrast']/180.0*np.pi)/2)
        print(mid-length/2, mid+length/2)
        img[:] = snap
        if mid-length/2>0:
            np.subtract(img, mid-length/2, out=img, casting='unsafe')
            np.multiply(img, 255.0/length, out=img, casting='unsafe')
        else:
            np.multiply(img, 255.0/length, out=img, casting='unsafe')
            np.subtract(img, (mid-length/2)/length*255, out=img, casting='unsafe')
        img[snap<mid-length/2] = 0
        img[snap>mid+length/2] = 255