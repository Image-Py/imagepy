# -*- coding: utf-8 -*-
"""
Created on Sat Dec 17 14:15:41 2016
@author: yxl
"""
import numpy as np
from imagepy.core.engine import Simple
from imagepy import IPy

class To8bit(Simple):
    title = '8-bit'
    note = ['all']

    def run(self, ips, imgs, para = None):
        if ips.imgtype == '8-bit': return
        n = ips.get_nslices()
        if ips.is3d:
            if ips.imgtype == 'rgb':
                img8 = np.zeros((n,) + ips.size, dtype=np.uint8)
                for i in range(n):
                    self.progress(i, len(imgs))
                    img8[i] = imgs[i].mean(axis=2)
            else:
                minv, maxv = ips.get_updown()
                k = 255.0/(max(1, maxv-minv))
                bf = np.clip(imgs, minv, maxv)
                img8 = ((bf - minv) * k).astype(np.uint8)
        else:
            img8 = []
            minv, maxv = ips.get_updown()
            for i in range(n):
                self.progress(i, len(imgs))
                if ips.imgtype == 'rgb':
                    img8.append(imgs[i].mean(axis=2).astype(np.uint8))
                else:
                    k = 255.0/(max(1, maxv-minv))
                    bf = np.clip(imgs[i], minv, maxv)
                    img8.append(((bf - minv) * k).astype(np.uint8))
        ips.set_imgs(img8)
        
class ToRGB(Simple):
    title = 'RGB'
    note = ['all']

    def run(self, ips, imgs, para = None):
        if ips.imgtype == 'rgb': return
        n = ips.get_nslices()
        if ips.is3d:
            imgrgb = np.zeros(ips.size+(n,), dtype=np.uint8)
            if ips.dtype == np.uint8: img8 = imgs
            else:
                minv, maxv = ips.get_updown()
                k = 255.0/(max(1, maxv-minv))
                bf = np.clip(imgs, minv, maxv)
                img8 = ((bf - minv) * k).astype(np.uint8)
            rgb = ips.lut[img8]
        else:
            rgb = []
            minv, maxv = ips.get_updown()
            for i in range(n):
                self.progress(i, len(imgs))
                if ips.dtype==np.uint8:
                    rgb.append(ips.lut[imgs[i]])
                else:
                    k = 255.0/(max(1, maxv-minv))
                    bf = np.clip(imgs[i], minv, maxv)
                    img8 = ((bf - minv) * k).astype(np.uint8)
                    rgb.append(ips.lut[img8])
        ips.set_imgs(rgb)

class ToUint16(Simple):
    title = '16-bit uint'
    note = ['all']

    def run(self, ips, imgs, para = None):
        if ips.imgtype == '16-bit': return
        n = ips.get_nslices()
        if ips.is3d:
            if ips.imgtype == 'rgb':
                img16 = imgs.mean(axis=3, dtype=np.uint16)
            else:
                img16 = np.clip(imgs, 0, 65535).astype(np.uint16)
        else:
            img16 = []
            minv, maxv = ips.get_updown()
            for i in range(n):
                self.progress(i, len(imgs))
                if ips.imgtype == 'rgb':
                    img16.append(imgs[i].mean(axis=2).astype(np.uint16))
                else:
                    k = 255.0/(max(1, maxv-minv))
                    img16.append(np.clip(imgs[i], 0, 65535).astype(np.uint16))
        ips.set_imgs(img16)

class ToInt32(Simple):
    title = '32-bit int'
    note = ['all']

    def run(self, ips, imgs, para = None):
        if ips.imgtype == '32-int': return
        n = ips.get_nslices()
        if ips.is3d:
            if ips.imgtype == 'rgb':
                img32 = imgs.mean(axis=3, dtype=np.int32)
            else:
                img32 = imgs.astype(np.int32)
        else:
            img32 = []
            minv, maxv = ips.get_updown()
            for i in range(n):
                self.progress(i, len(imgs))
                if ips.imgtype == 'rgb':
                    img32.append(imgs[i].mean(axis=2).astype(np.int32))
                else:
                    k = 255.0/(max(1, maxv-minv))
                    img32.append(imgs[i].astype(np.int32))
        ips.set_imgs(img32)

class ToFloat32(Simple):
    title = '32-bit float'
    note = ['all']

    def run(self, ips, imgs, para = None):
        if ips.imgtype == '32-float': return
        n = ips.get_nslices()
        if ips.is3d:
            if ips.imgtype == 'rgb':
                img32 = imgs.mean(axis=3, dtype=np.float32)
            else:
                img32 = imgs.astype(np.float32)
        else:
            img32 = []
            minv, maxv = ips.get_updown()
            for i in range(n):
                self.progress(i, len(imgs))
                if ips.imgtype == 'rgb':
                    img32.append(imgs[i].mean(axis=2).astype(np.float32))
                else:
                    k = 255.0/(max(1, maxv-minv))
                    img32.append(imgs[i].astype(np.float32))
        ips.set_imgs(img32)

class ToFloat64(Simple):
    title = '64-bit float'
    note = ['all']

    def run(self, ips, imgs, para = None):
        if ips.imgtype == '64-bit': return
        n = ips.get_nslices()
        if ips.is3d:
            if ips.imgtype == 'rgb':
                img64 = imgs.mean(axis=3, dtype=np.float64)
            else:
                img64 = imgs.astype(np.float64)
        else:
            img64 = []
            minv, maxv = ips.get_updown()
            for i in range(n):
                self.progress(i, len(imgs))
                if ips.imgtype == 'rgb':
                    img64.append(imgs[i].mean(axis=2).astype(np.float64))
                else:
                    k = 255.0/(max(1, maxv-minv))
                    img64.append(imgs[i].astype(np.float64))
        ips.set_imgs(img64)
        
plgs = [To8bit, ToRGB, '-', ToUint16, ToInt32, ToFloat32, ToFloat64]