# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 00:56:00 2016
@author: yxl
"""

from imagepy import IPy
import numpy as np
from imagepy.core.engine import Filter, Simple
from imagepy.core.manager import WindowsManager

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

def match(img1, img2):
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
        
class Match(Simple):
    """Calculator Plugin derived from imagepy.core.engine.Simple """
    title = 'Histogram Match'
    note = ['all']
    para = {'img1':'', 'img2':''}
    
    def load(self, ips):
        titles = WindowsManager.get_titles()
        self.para['img1'] = titles[0]
        self.para['img2'] = titles[0]
        Match.view = [(list, titles, str, 'template', 'img1', ''),
                       (list, titles, str, 'object', 'img2', '')]
        return True
    
    def run(self, ips, imgs, para = None):
        ips1 = WindowsManager.get(para['img1']).ips
        ips2 = WindowsManager.get(para['img2']).ips
        ips2.snapshot()

        img = ips1.img
        imgs = ips2.imgs

        sl1, sl2 = ips1.get_nslices(), ips2.get_nslices()
        cn1, cn2 = ips1.get_nchannels(), ips2.get_nchannels()
        if not(ips1.img.dtype == np.uint8 and ips2.img.dtype == np.uint8):
            IPy.alert('Two image must be type of 8-bit or rgb!')
            return
        
        for i in range(sl2):
            self.progress(i, sl2)
            match(img, imgs[i])
        ips2.update = 'pix'

plgs = [Normalize, Match]