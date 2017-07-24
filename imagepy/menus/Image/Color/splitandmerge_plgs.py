# -*- coding: utf-8 -*-
"""
Created on Sat Dec 17 10:49:15 2016
@author: yxl
"""
from imagepy import IPy
import numpy as np
from imagepy import ImagePlus
from imagepy.ui.canvasframe import CanvasFrame
from imagepy.core.manager import WindowsManager
from imagepy.core.engine import Simple

class Split(Simple):
    title = 'Split Channels'
    note = ['rgb']
    
    para = {'copy':False, 'destory':True}
    view = {(bool, 'Copy data from view', 'copy'),
            (bool, 'Destory current image', 'destory')}
    #process
    def run(self, ips, imgs, para = None):
        r,g,b = [],[],[]
        for i,n in zip(imgs,list(range(ips.get_nslices()))):
            self.progress(i, n)
            for c,ci in zip((r,g,b),(0,1,2)):
                if self.para['copy']:c.append(i[:,:,ci].copy())
                else: c.append(i[:,:,ci])
        for im, tl in zip([r,g,b],['red','green','blue']):
            IPy.show_img(im, ips.title+'-'+tl)
        if self.para['destory']:
            WindowsManager.close(ips.title)

class Merge(Simple):
    title = 'Merge Channels'
    note = ['all']
    
    #parameter
    para = {'red':'','green':'','blue':'','destory':True}
    
    def load(self, ips):
        titles = WindowsManager.get_titles()
        self.para['red'] = titles[0]
        self.para['green'] = titles[0]
        self.para['blue'] = titles[0]
        Merge.view = [(list, titles, str, 'Red', 'red', ''),
                       (list, titles, str, 'Green', 'green', ''),
                       (list, titles, str, 'Blue', 'blue', ''),
                       (bool, 'Destory r,g,b image', 'destory')]
        return True
    
    def run(self, ips, imgs, para = None):
        idx = ['red','green','blue']
        imr,img,imb = [WindowsManager.get(para[i]).ips for i in idx]
        sr,sg,sb = [i.get_nslices() for i in [imr,img,imb]]
        
        if imr.imgtype!='8-bit' or img.imgtype!='8-bit' or imb.imgtype!='8-bit':
            IPy.alert('must be three 8-bit image!')
            return
        if imr.size!=img.size or img.size!=imb.size or sr!=sg or sg!=sb:
            IPy.alert('three image must be in same size and have the same slices!')
            return
            
        rgb = []
        w,h = imr.size
        rgbs = list(zip(imr.imgs,img.imgs,imb.imgs))
        for i in range(sr):
            self.progress(i,sr)
            img = np.zeros((w,h,3), dtype=np.uint8)
            for j in (0,1,2):img[:,:,j] = rgbs[i][j]
            rgb.append(img)
        IPy.show_img(rgb, 'rgb-merge')
        if self.para['destory']:
            for title in [para[i] for i in idx]:
                WindowsManager.close(title)

plgs = [Split, Merge]