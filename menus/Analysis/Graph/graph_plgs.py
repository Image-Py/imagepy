# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 22:05:43 2016

@author: yxl
"""

import numpy as np
from core.engines import Filter
from core.graph import builder
from scipy.ndimage.filters import convolve
import IPy

loc = np.array([(1,0),(1,1),(0,1),(-1,1),
        (-1,0),(-1,-1),(0,-1),(1,-1),(1,0)])

class Marker(Filter):
    title = 'Mark Graph'
    note = ['8-bit', 'auto_snap', 'preview']

    #process
    def run(self, ips, snap, img, para = None):
        core = np.array([[1,1,1],[1,0,1],[1,1,1]])
        msk = snap>0
        convolve(msk, core, output=img)
        np.clip(img*msk, 0, 3, out=img)
        pts = np.array(np.where(img==3)).T
        print 'len', len(pts)
        for p in pts:
            idx = (loc+p).T
            v = img[idx[0], idx[1]]
            #print np.sum((v[:-1]==0)*(v[1:]>0))
            if np.sum((v[:-1]==0)*(v[1:]>0))==2:
                img[tuple(p)] = 2
        img[:] = np.array([0,255,128,255], dtype=np.uint8)[img]

class Builder(Filter):
    title = 'Build Graph'
    note = ['8-bit', 'not_slice', 'auto_snap', 'preview']

    #process
    def run(self, ips, snap, img, para = None):
        rst = builder.build(img/127)
        data = []
        for i in rst:
            data.append([len(i[0]), len(i[1])])
        print data
        IPy.table('Graph Builder', data, ['nodes','arcs'])

plgs = [Marker, Builder]