"""
Created on Sun Jan 25 9:00:00 2020
@author: weisong
"""
from imagepy.core.engine import Simple
import numpy as np
from imagepy import IPy

class Plugin(Simple):
    title = 'Normalize'
    note = ['8-bit','16-bit','float','stack']
    para = {'if3d': False, 'Sb':False}
    view = [(bool, 'if3d', '3D stack'),
    (bool, 'Sb', 'Subtract background')]

    def run(self, ips, imgs, para = None):
        imgs_=imgs.astype('float64')
        if para['if3d']:
            if para['Sb']:
                 imgs_ -= imgs_.min()
            imgs_ = imgs_ / imgs_.max()
        else:
            if para['Sb']:
                 for i in range(len(imgs_)):
                     imgs_[i] -= imgs_[i].min()
            for i in range(len(imgs_)):
                imgs_[i] = imgs_[i] / imgs_[i].max()
        if imgs.dtype == np.uint8:
            imgs[:] = (255*imgs_).astype(imgs.dtype)
        elif imgs.dtype == np.uint16:
            imgs[:] = (65535*imgs_).astype(imgs.dtype)
        else:
            imgs[:] = (imgs_).astype(imgs.dtype)