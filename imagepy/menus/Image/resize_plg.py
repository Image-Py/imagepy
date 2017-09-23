# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 23:03:28 2016
@author: yxl
"""

from imagepy.core.engine import Simple
import scipy.ndimage as ndimg
import numpy as np
from imagepy import IPy

class Plugin(Simple):
    title = 'Resize'
    note = ['all']
    
    para = {'kx':0.5, 'ky':0.5, 'kz':1}
    view = [(float, (0.1,10), 1, 'kx', 'kx', '0.1~10'),
            (float, (0.1,10), 1, 'ky', 'ky', '0.1~10'),
            (float, (0.1,10), 1, 'kz', 'kz', '0.1~10'),
            ('lab', 'the kz only works on stack!')]
    
    def run(self, ips, imgs, para = None):
        kx, ky, kz = [para[i] for i in ('ky','kx','kz')]
        size = np.round([ips.width*kx, ips.height*ky])
        w, h = size.astype(np.uint16)
        if ips.is3d:
            if ips.get_nchannels()>1:
                new = np.zeros(np.multiply(imgs.shape, 
                    (kz, kx, ky, 1)).round().astype(np.uint32), dtype=imgs.dtype)
                for i in range(ips.get_nchannels()):
                    ndimg.zoom(imgs[:,:,:,i], (kz, kx, ky), output=new[:,:,:,i])
            else :
                new = ndimg.zoom(imgs, (kz, kx, ky))
        else:
            if ips.get_nchannels()>1:
                new = []
                for i in range(len(imgs)):
                    self.progress(i, len(imgs))
                    arr = np.zeros(np.multiply(imgs[i].shape, 
                        (kx, ky, 1)).round().astype(np.uint32),  dtype=imgs[i].dtype)
                    for n in range(ips.get_nchannels()):
                        ndimg.zoom(imgs[i][:,:,n], (kx, ky), output=arr[:,:,n])
                    new.append(arr)
            else :
                new = []
                for i in range(len(imgs)):
                    self.progress(i, len(imgs))
                    arr = ndimg.zoom(imgs[i], (kx, ky))
                    new.append(arr)

        ips.set_imgs(new)
        backimg = ips.backimg
        if backimg is None:return
        if backimg.ndim == 3:
            nbc = np.zeros(np.multiply(backimg.shape, 
                (kx, ky, 1)).round().astype(np.uint32), dtype=np.uint8)
            for i in range(3):
                ndimg.zoom(backimg[:,:,i], (kx, ky), output=nbc[:,:,i])
            print(nbc.dtype)
        else :
            nbc = ndimg.zoom(backimg, (kz, kx))
            print(nbc.dtype)
        ips.backimg = nbc