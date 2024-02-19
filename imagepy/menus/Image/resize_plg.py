# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 23:03:28 2016
@author: yxl
"""

from sciapp.action import Simple
import scipy.ndimage as ndimg
import numpy as np

class Plugin(Simple):
    title = 'Resize'
    note = ['all']
    
    para = {'kx':0.5, 'ky':0.5, 'kz':1,'order':3}
    view = [(float, 'kx', (0.1,10), 2, 'kx', '0.1~10'),
            (float, 'ky', (0.1,10), 2, 'ky', '0.1~10'),
            (float, 'kz', (0.1,10), 2, 'kz', '0.1~10'),
            (int, 'order', (0,5), 0, 'accu', '0-5'),
            ('lab',  None, 'the kz only works on stack!')]
    
    def run(self, ips, imgs, para = None):
        kx, ky, kz = [para[i] for i in ('ky','kx','kz')]
        size = np.round([ips.slices*kz, ips.shape[1]*kx, ips.shape[0]*ky])
        n, w, h = size.astype(np.uint16)

        buf = np.zeros((n, h, w, ips.channels), dtype=ips.dtype)
        if kz==1:
            for i in range(ips.slices):
                img = imgs[i].reshape(ips.shape+(-1,))
                for c in range(ips.channels):
                    ndimg.zoom(img[:,:,c], (ky, kx), output=buf[i,:,:,c], order=para['order'])
        else: 
            for c in range(ips.channels):
                imgsc = [i.reshape(i.shape[:2]+(-1,))[:,:,c] for i  in imgs]
                ndimg.zoom(imgsc, (kz, kx, ky), order=para['order'], output=buf[:,:,:,c])

        if ips.channels == 1: buf.shape = (buf.shape[:3])
        if n == 1: buf = [buf.reshape(buf.shape[1:])]
        ips.set_imgs(buf)
        '''
        else: 

        if ips.slice>1:
            if ips.channels>1:
                new = np.zeros(np.multiply(imgs.shape, 
                    (kz, kx, ky, 1)).round().astype(np.uint32), dtype=imgs.dtype)
                for i in range(ips.channels):
                    ndimg.zoom(imgs[:,:,:,i], (kz, kx, ky), output=new[:,:,:,i], order=para['order'])
            else :
                new = ndimg.zoom(imgs, (kz, kx, ky), order=para['order'])
        else:
            if ips.channels>1:
                new = []
                for i in range(len(imgs)):
                    self.progress(i, len(imgs))
                    arr = np.zeros(np.multiply(imgs[i].shape, 
                        (kx, ky, 1)).round().astype(np.uint32),  dtype=imgs[i].dtype)
                    for n in range(ips.channels:
                        ndimg.zoom(imgs[i][:,:,n], (kx, ky), output=arr[:,:,n], order=para['order'])
                    new.append(arr)
            else :
                new = []
                for i in range(len(imgs)):
                    self.progress(i, len(imgs))
                    arr = ndimg.zoom(imgs[i], (kx, ky), order=para['order'])
                    new.append(arr)

        ips.set_imgs(new)
        return
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
        '''