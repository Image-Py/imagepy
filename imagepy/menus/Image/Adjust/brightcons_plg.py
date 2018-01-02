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
    def init_view(self, items, para, hist):
        self.histcvs = HistCanvas(self)
        self.histcvs.set_hist(hist)
        self.add_ctrl('hist', self.histcvs)
        ParaDialog.init_view(self, items, para, True)
    
    def para_check(self, para, key):
        mid = 128-para['bright']
        length = 255/np.tan(para['contrast']/180.0*np.pi)
        self.histcvs.set_lim(mid-length/2, mid+length/2)
        self.reset()
        return True
        
class Plugin(Filter):
    title = 'Bright And Constract'
    note = ['all', 'auto_msk', 'auto_snap', 'not_channel', 'preview']
        
    def load(self, ips):
        if ips.imgtype in ('8-bit', 'rgb'):
            self.para = {'bright':0, 'contrast':45}
            self.view = [('slide', (-100,100), 'Brightness', 'bright', ''),
                ('slide', (1,89), 'Contrast', 'contrast', '')]
            if 'not_slice' in self.note:
                self.note.remove('not_slice')
        else :
            self.arange = minv, maxv = ips.img.min(), ips.img.max()
            self.para = {'bright':np.mean(ips.range) - np.mean(self.arange), 
                'contrast':round(np.arctan((maxv-minv)/(ips.range[1]-ips.range[0]))/np.pi*180)}
            self.view = [('slide', (-(maxv-minv)/2, (maxv-minv)/2), 'Brightness', 'bright', ''),
                ('slide', (1,89), 'Contrast', 'contrast', '')]
            if not 'not_slice' in self.note:
                self.note.append('not_slice')
        return True

    def show(self):
        self.dialog = ThresholdDialog(IPy.get_window(), self.title)
        hist = np.histogram(self.ips.lookup(),list(range(257)))[0]
        self.dialog.init_view(self.view, self.para, hist)
        self.dialog.set_handle(lambda x:self.preview(self.ips, self.para))
        return self.dialog.ShowModal()

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