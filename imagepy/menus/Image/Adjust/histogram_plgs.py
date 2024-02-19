# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 00:56:00 2016
@author: yxl
"""
import numpy as np
from sciapp.action import Filter, Simple

def like(hist1, hist2):
    hist1 = np.cumsum(hist1)/hist1.sum()
    hist2 = np.cumsum(hist2)/hist2.sum()
    hist = np.zeros(256, dtype=np.uint8)
    i1, i2, s = 0, 0, 0
    while i2<256:
        while i1<256 and hist2[i2]>hist1[i1]:i1+=1
        hist[i2] = i1
        i2+=1
    return hist

def match(img2, img1):
    if img1.ndim == 2:
        temp = np.histogram(img1, np.arange(257))[0]
        if img2.ndim == 2:
            hist = np.histogram(img2, np.arange(257))[0]
            ahist = like(temp, hist)
            img2[:] = ahist[img2]
        if img2.ndim == 3:
            for i in range(3):
                hist = np.histogram(img2[:,:,i], np.range(257))[0]
                ahist = like(temp, hist)
                img2[:,:,i] = ahist[img2[:,:,i]]
    elif img1.ndim == 3:
        if img2.ndim == 2:
            temp = np.histogram(img1, np.arange(257))[0]
            hist = np.histogram(img2, np.arange(257))[0]
            ahist = like(temp, hist)
            img2[:] = ahist[img2]
        if img2.ndim == 3:
            for i in range(3):
                temp = np.histogram(img1[:,:,i], np.arange(257))[0]
                hist = np.histogram(img2[:,:,i], np.arange(257))[0]
                ahist = like(temp, hist)
                img2[:,:,i] = ahist[img2[:,:,i]]

class Normalize(Filter):
    title = 'Histogram Normalize'
    note = ['8-bit', 'rgb', 'auto_snap']

    def run(self, ips, snap, img, para = None):
        temp = np.ones(256)
        hist = np.histogram(img, np.arange(257))[0]
        ahist = like(temp, hist)
        img[:] = ahist[img]
        
class Match(Filter):
    """Calculator Plugin derived from sciapp.action.Simple """
    title = 'Histogram Match'
    note = ['all', 'not_channel', 'auto_snap', 'auto_msk']
    para = {'img':None}
    view = [('img', 'img', 'temp', '')]
    
    def run(self, ips, snap, img, para = None):
        temp = self.app.get_img(para['img']).img
        if not(ips.dtype == np.uint8 and temp.dtype == np.uint8):
            return self.app.alert('Two image must be type of 8-bit or rgb!')
        match(img, temp)

plgs = [Normalize, Match]