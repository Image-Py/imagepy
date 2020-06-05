# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 17:35:09 2016

@author: yxl
"""

from imagepy.core.engine import Tool
import numpy as np
from sciapp import Source
# from imagepy.core.draw.fill import floodfill
from skimage.morphology import flood_fill, flood

class Plugin(Tool):
    title = 'Flood Fill'
    para = {'tor':10, 'con':'8-connect'}
    view = [(int, 'tor', (0,1000), 0, 'torlorance', 'value'),
            (list, 'con', ['4-connect', '8-connect'], str, 'fill', 'pix')]
        
    def mouse_down(self, ips, x, y, btn, **key):
        
        img, color = ips.img, Source.manager('color').get('front')
        if int(y)<0 or int(x)<0: return
        if int(y)>=img.shape[0] or int(x)>=img.shape[1]: return 

        ips.snapshot()
        connectivity=(self.para['con']=='8-connect')+1
        img = ips.img.reshape((ips.img.shape+(1,))[:3])
        msk = np.ones(img.shape[:2], dtype=np.bool)
        for i in range(img.shape[2]):
            msk &= flood(img[:,:,i], (int(y),int(x)), 
                connectivity=connectivity, tolerance=self.para['tor'])
        img[msk] = np.mean(color) if img.shape[2]==1 else color
        ips.update()
    
    def mouse_up(self, ips, x, y, btn, **key):
        pass
    
    def mouse_move(self, ips, x, y, btn, **key):
        pass
        
    def mouse_wheel(self, ips, x, y, d, **key):
        pass

