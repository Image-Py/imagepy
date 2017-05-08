# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 22:05:43 2016

@author: yxl
"""

import numpy as np
from core.engine import Filter
from core.graph import builder
from scipy.ndimage.filters import convolve
import IPy

'''    
def mark(img):
    lo = np.array([[-1,-1,-1,0,0,1,1,1],
                    [-1,0,1,-1,1,-1,0,1]])
    arr = convolve(img, np.ones((3,3)))
    arr = np.clip((arr-1)*img, 0,3)
    pts = np.array(np.where(arr==3)).T
    for p in pts:
        
        idx = (lo.T+p).T
        v = arr[idx[0], idx[1]]>0
        fac = np.array([1,2,4,8,16,32,64,128])
        c = lut[np.dot(v, fac)]
        if c==0: arr[tuple(p)] = 0
    pts = np.array(np.where(arr==3)).T
    for p in pts:
        if arr[tuple(p)]==0:continue
        idx = (lo.T+p).T
        v = arr[idx[0], idx[1]]>0
        fac = np.array([1,2,4,8,16,32,64,128])
        c = lut[np.dot(v, fac)]
        if c==1: arr[tuple(p)] = 2
    img[:] = np.array([0,255,128,255])[arr]
'''
class Marker(Filter):
    title = 'Mark Graph'
    note = ['8-bit', 'auto_snap', 'preview']

    #process
    def run(self, ips, snap, img, para = None):
        builder.mark(img)

class Builder(Filter):
    title = 'Build Graph'
    note = ['8-bit', 'not_slice', 'auto_snap', 'preview']

    #process
    def run(self, ips, snap, img, para = None):
        rst = builder.build_graph(img/127)
        data = []
        for i in rst:
            data.append([len(i[0]), len(i[1])])
        print data
        IPy.table('Graph Builder', data, ['nodes','arcs'])

plgs = [Marker, Builder]