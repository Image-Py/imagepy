# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 01:57:11 2016
@author: yxl
"""
import numpy as np
from sciapp.action import Simple

class ToStack(Simple):
    title = 'Trans to Stack'
    note = ['all','no_change','req_stack']

    def run(self, ips, imgs, para = None):
        ips.imgs = np.asarray(imgs)
        '''
        ips.imgs = np.array()
        imgstack = np.zeros((ips.slices,) + ips.shape, dtype=ips.dtype)
        for i in range(ips.get_nslices()):
            imgstack[i] = ips.imgs[i]
        ips.imgs = imgstack
        ips.is3d = True
        '''
        
class ToList(Simple):
    title = 'Trans to List'
    note = ['all','no_change','req_stack']

    def run(self, ips, imgs, para = None):
        ips.imgs = list(imgs)
        
plgs = [ToStack, ToList]