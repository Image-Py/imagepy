# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 01:22:19 2016

@author: yxl
"""
from core.managers import WindowsManager
import IPy

from core.engines import Simple
from core.pixcel import bliter

class Plugin(Simple):
    title = 'Image Calculator'
    note = ['all']
    
    #parameter
    para = {'img1':'','op':'add','img2':''}
    
    def load(self, ips):
        titles = WindowsManager.get_titles()
        self.para['img1'] = titles[0]
        self.para['img2'] = titles[0]
        Plugin.view = [(list, titles, str, 'image1', 'img1', ''),
            (list, ['max', 'min', 'diff', 'add', 'substract'], str, 'operator', 'op',''),
            (list, titles, str, 'image2', 'img2', '')]
        return True
    
    #process
    def run(self, ips, imgs, para = None):
        ips1 = WindowsManager.get(para['img1']).ips
        ips2 = WindowsManager.get(para['img2']).ips

        sl1, sl2 = ips1.get_nslices(), ips2.get_nslices()
        cn1, cn2 = ips1.get_nchannels(), ips2.get_nchannels()
        if ips1.dtype != ips2.dtype:
            IPy.alert('Two stack must be equal dtype!')
            return
        elif sl1>1 and sl2>1 and sl1!=sl2:
            IPy.alert('Two stack must have equal slices!')
            return
        elif cn1>1 and cn2>1 and cn1!=cn2:
            IPy.alert('Two stack must have equal chanels!')
            return
            
        w, h = ips1.size, ips2.size
        w, h = min(w[0], h[0]), min(w[1], h[1])
        if sl1 == 1:
            bliter.blit(ips1.get_img(), ips2.get_img(), mode=para['op'])
        elif sl1>1 and sl2==1:
            for i in range(sl1):
                IPy.set_progress(round(i*100.0/sl1))
                bliter.blit(ips1.imgs[i], ips2.get_img(), mode=para['op'])
        elif sl1>1 and sl2>1:
            for i in range(sl1):
                IPy.set_progress(round(i*100.0/sl1))
                bliter.blit(ips1.imgs[i], ips2.imgs[i], mode=para['op'])
        IPy.set_progress(0)
        ips1.update = 'pix'
        