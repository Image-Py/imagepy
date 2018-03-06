# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 01:22:19 2016
@author: yxl
"""
from imagepy.core.manager import WindowsManager
from imagepy import IPy

from imagepy.core.engine import Simple
from imagepy.core.pixel import bliter

class Plugin(Simple):
    """Calculator Plugin derived from imagepy.core.engine.Simple """
    title = 'Image Calculator'
    note = ['all']
    para = {'img1':'','op':'add','img2':''}
    
    def load(self, ips):
        titles = WindowsManager.get_titles()
        self.para['img1'] = titles[0]
        self.para['img2'] = titles[0]
        Plugin.view = [(list, titles, str, 'image1', 'img1', ''),
                       (list, ['max', 'min', 'diff', 'add', 'substract'
                               ], str, 'operator', 'op',''),
                       (list, titles, str, 'image2', 'img2', '')]
        return True
    
    def run(self, ips, imgs, para = None):
        ips1 = WindowsManager.get(para['img1']).ips
        ips2 = WindowsManager.get(para['img2']).ips
        ips1.snapshot()

        sl1, sl2 = ips1.get_nslices(), ips2.get_nslices()
        cn1, cn2 = ips1.get_nchannels(), ips2.get_nchannels()
        if ips1.dtype != ips2.dtype:
            IPy.alert('Two stack must be equal dtype!')
            return
        elif sl1>1 and sl2>1 and sl1!=sl2:
            IPy.alert('Two stack must have equal slices!')
            return
        elif cn1>1 and cn2>1 and cn1!=cn2:
            IPy.alert('Two stack must have equal channels!')
            return
            
        w, h = ips1.size, ips2.size
        w, h = min(w[0], h[0]), min(w[1], h[1])
        if sl1 == 1:
            bliter.blit(ips1.get_subimg(), ips2.get_subimg(), mode=para['op'])
        elif sl1>1 and sl2==1:
            for i in range(sl1):
                self.progress(i, sl1)
                ss1, se1 = ips1.get_rect()
                bliter.blit(ips1.imgs[i][ss1, se1], ips2.get_subimg(), mode=para['op'])
        elif sl1>1 and sl2>1:
            for i in range(sl1):
                self.progress(i, sl1)
                ss1, se1 = ips1.get_rect()
                ss2, se2 = ips2.get_rect()
                bliter.blit(ips1.imgs[i][ss1, se1], ips2.imgs[i][ss2, se2], mode=para['op'])
        ips1.update = 'pix'
        