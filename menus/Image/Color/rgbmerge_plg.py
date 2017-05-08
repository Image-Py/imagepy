# -*- coding: utf-8 -*-
"""
Created on Sat Dec 17 10:49:15 2016

@author: yxl
"""

from core.engine import Simple
from imageplus import ImagePlus
from ui.canvasframe import CanvasFrame
from core.manager import WindowsManager
import numpy as np
import IPy

class Plugin(Simple):
    title = 'Merge Channels'
    note = ['all']
    
    #parameter
    para = {'red':'','green':'','blue':'','destory':True}
    
    def load(self, ips):
        titles = WindowsManager.get_titles()
        self.para['red'] = titles[0]
        self.para['green'] = titles[0]
        self.para['blue'] = titles[0]
        Plugin.view = [(list, titles, str, 'Red', 'red', ''),
                       (list, titles, str, 'Green', 'green', ''),
                        (list, titles, str, 'Blue', 'blue', ''),
                        (bool, 'Destory r,g,b image', 'destory')]
        return True
    #process
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
        rgbs = zip(imr.imgs,img.imgs,imb.imgs)
        for i in range(sr):
            IPy.curapp.set_progress(round((i+1)*100.0/sr))
            img = np.zeros((w,h,3), dtype=np.uint8)
            for j in (0,1,2):img[:,:,j] = rgbs[i][j]
            rgb.append(img)
        IPy.curapp.set_progress(0)
        ip = ImagePlus(rgb, 'rgb-merge')
        frame = CanvasFrame(IPy.curapp)
        frame.set_ips(ip)
        frame.Show()
        if self.para['destory']:
            for title in [para[i] for i in idx]:
                WindowsManager.close(title)