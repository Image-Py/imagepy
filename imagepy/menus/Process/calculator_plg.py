# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 01:22:19 2016
@author: yxl
"""
from imagepy.core.engine import Simple
from imagepy.core.pixel import bliter

class Plugin(Simple):
    """Calculator Plugin derived from imagepy.core.engine.Simple """
    title = 'Image Calculator'
    note = ['all']
    para = {'img1':None,'op':'add','img2':None}
    
    view = [('img', 'img1', 'image1', ''),
            (list, 'op', ['max', 'min', 'diff', 'add', 'substract'], str, 'operator', ''),
            ('img', 'img2', 'image2', '')]
    
    def run(self, ips, imgs, para = None):
        ips1 = self.app.get_img(para['img1'])
        ips2 = self.app.get_img(para['img2'])
        ips1.snapshot()

        sl1, sl2 = ips1.slices, ips2.slices
        cn1, cn2 = ips1.channels, ips2.channels
        if ips1.dtype != ips2.dtype:
            return self.app.alert('Two stack must be equal dtype!')
        elif sl1>1 and sl2>1 and sl1!=sl2:
            return self.app.alert('Two stack must have equal slices!')
        elif cn1>1 and cn2>1 and cn1!=cn2:
            return self.app.alert('Two stack must have equal channels!')
            
        w, h = ips1.shape, ips2.shape
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
        ips1.update()
        