# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 01:22:19 2016
@author: yxl
"""
from imagepy.core.manager import WindowsManager
from imagepy import IPy
import numpy as np
from imagepy.core.engine import Simple

class SetBackground(Simple):
    """Calculator Plugin derived from imagepy.core.engine.Simple """
    title = 'Set Background'
    note = ['all']
    para = {'img':'None','op':'Mean', 'k':0.5, 'kill':False}
    view = [('img','background', 'img', '8-bit'),
            (list, ['Mean', 'Clip'], str, 'mode', 'op',''),
            (float, (0,1), 1, 'blender', 'k', ''),
            (bool, 'kill', 'kill')]
    
    def run(self, ips, imgs, para = None):
        if para['kill']:
            ips.backimg = None
        else:
            img = WindowsManager.get(para['img']).ips.img
            if img.dtype != np.uint8 or img.shape[:2] != ips.img.shape[:2]:
                IPy.alert('a background image must be 8-bit and with the same size')
                return
            ips.backimg = img
            ips.backmode = (para['k'], para['op'])
        ips.update = 'pix'
        
class BackgroundSelf(Simple):
    """Calculator Plugin derived from imagepy.core.engine.Simple """
    title = 'Background Self'
    note = ['8-bit', 'rgb']
    para = {'op':'Mean', 'k':0.5, 'kill':False}
    view = [(list, ['Mean', 'Clip'], str, 'mode', 'op',''),
            (float, (0,1), 1, 'blender', 'k', ''),
            (bool, 'kill', 'kill')]
    
    def run(self, ips, imgs, para = None):
        if para['kill']:
            ips.backimg = None
        else:
            ips.backimg = ips.img.copy()
            ips.backmode = (para['k'], para['op'])
        ips.update = 'pix'

plgs = [SetBackground, BackgroundSelf]