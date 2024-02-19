# -*- coding: utf-8 -*-
"""
Created on Sat Dec 17 14:15:41 2016
@author: yxl
"""
import numpy as np
from sciapp.action import Simple

def trans(imgs, shp, cn, sl, rg1, rg2, tp, prog=print):
    buf = np.zeros(shp, dtype=np.float32)
    (x1, x2), (y1, y2) = rg1, rg2
    if x1 == x2: x1, x2 = x1-1e-8, x2+1e-8
    if y1 == y2: y1, y2 = y1-1e-8, y2+1e-8
    k, b = np.dot(np.linalg.inv([[x1,1],[x2,1]]), [[y1],[y2]]).ravel()

    rst = [None]*sl if isinstance(imgs, list) else np.zeros((sl,)+shp, dtype=tp)
    for i in range(sl):
        if cn == 1: buf[:] = imgs[i]
        else: imgs[i].mean(axis=-1, out=buf)
        if rg1 != rg2:
            buf *= k
            buf += b
        if isinstance(imgs, list):
            rst[i] = np.clip(buf, y1, y2).astype(tp)
        else: np.clip(buf, y1, y2, out=tp)
    return rst

class To8bit(Simple):
    title = '8-bit'
    note = ['all']

    def run(self, ips, imgs, para = None):
        if ips.dtype == np.uint8 and ips.channels == 1: return
        ips.set_imgs(trans(imgs, ips.shape, ips.channels, ips.slices, ips.range, (0,255), np.uint8))
        
class ToRGB(Simple):
    title = 'RGB'
    note = ['all']

    def run(self, ips, imgs, para = None):
        if ips.dtype == np.uint8 and ips.channels == 3: return
        n = ips.slices

        if ips.isarray:
            imgrgb = np.zeros(ips.size+(n,), dtype=np.uint8)
            if ips.dtype == np.uint8: img8 = imgs
            else:
                minv, maxv = ips.range
                k = 255.0/(max(1e-8, maxv-minv))
                bf = np.clip(imgs, minv, maxv)
                img8 = ((bf - minv) * k).astype(np.uint8)
            rgb = ips.lut[img8]
        else:
            rgb = []
            minv, maxv = ips.range
            for i in range(n):
                self.progress(i, len(imgs))
                if ips.dtype==np.uint8:
                    rgb.append(ips.lut[imgs[i]])
                else:
                    k = 255.0/(max(1e-8, maxv-minv))
                    bf = np.clip(imgs[i], minv, maxv)
                    img8 = ((bf - minv) * k).astype(np.uint8)
                    rgb.append(ips.lut[img8])
        ips.set_imgs(rgb)

class ToUint16(Simple):
    title = '16-bit uint'
    note = ['all']

    def run(self, ips, imgs, para = None):
        if ips.dtype == np.uint16 and ips.channels == 1: return
        ips.set_imgs(trans(imgs, ips.shape, ips.channels, ips.slices, ips.range, (0,65535), np.uint16))


class ToInt32(Simple):
    title = '32-bit int'
    note = ['all']

    def run(self, ips, imgs, para = None):
        if ips.dtype == np.int32 and ips.channels == 1: return
        ips.set_imgs(trans(imgs, ips.shape, ips.channels, ips.slices, ips.range, ips.range, np.int32))

class ToFloat32(Simple):
    title = '32-bit float'
    note = ['all']

    def run(self, ips, imgs, para = None):
        if ips.dtype == np.float32 and ips.channels == 1: return
        ips.set_imgs(trans(imgs, ips.shape, ips.channels, ips.slices, ips.range, ips.range, np.float32))

class ToFloat64(Simple):
    title = '64-bit float'
    note = ['all']

    def run(self, ips, imgs, para = None):
        if ips.dtype == np.float64 and ips.channels == 1: return
        ips.set_imgs(trans(imgs, ips.shape, ips.channels, ips.slices, ips.range, ips.range, np.float64))

plgs = [To8bit, ToRGB, '-', ToUint16, ToInt32, ToFloat32, ToFloat64]