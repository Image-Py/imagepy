"""
Created on Sun Nov 27 00:56:00 2016
@author: yxl
"""
import numpy as np
from sciapp.action import Filter
#from imagepy.ui.widgets import HistCanvas
        
class Plugin(Filter):
    title = 'Bright And Constract'
    note = ['all', 'auto_msk', 'auto_snap', 'not_channel', 'preview']
        
    def load(self, ips):
        hist = ips.histogram(chans='all', step=512)
        if ips.dtype == np.uint8:
            self.para = {'b_c':(0, 45)}
            self.view = [('hist', 'b_c', 'bc', hist, (-255, 255), 0)]
        else :
            self.rrange = minv, maxv = ips.img.min(), ips.img.max()
            self.para = {'bright':np.mean(ips.range) - np.mean(self.range), 
                'contrast':round(np.arctan((maxv-minv)/(ips.range[1]-ips.range[0]))/np.pi*180)}
            self.view = [('hist', 'b_c', 'bc', hist, (-(maxv-minv)/2, (maxv-minv)/2), 10)]
        self.lut = ips.lut
        return True

    #process
    def run(self, ips, snap, img, para = None):
        bright, contrast = para['b_c']
        if not ips.dtype == np.uint8:
            mid = (self.arange[0] + self.arange[1])/2 - bright
            length = (self.arange[1] - self.arange[0])/np.tan(contrast/180.0*np.pi)
            ips.range = (mid-length/2, mid+length/2)
            return
        if para == None: para = self.para
        mid = 128-bright
        length = 255/np.tan(contrast/180.0*np.pi)
        img[:] = snap
        if mid-length/2>0:
            np.subtract(img, mid-length/2, out=img, casting='unsafe')
            np.multiply(img, 255.0/length, out=img, casting='unsafe')
        else:
            np.multiply(img, 255.0/length, out=img, casting='unsafe')
            np.subtract(img, (mid-length/2)/length*255, out=img, casting='unsafe')
        img[snap<mid-length/2] = 0
        img[snap>mid+length/2] = 255