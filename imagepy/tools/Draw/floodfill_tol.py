# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 17:35:09 2016

@author: yxl
"""

from imagepy.core.engine import Tool
import numpy as np
from imagepy.core.manager import ColorManager
from imagepy.core.draw.fill import floodfill

class Plugin(Tool):
    title = 'Flood Fill'
    para = {'tor':10, 'con':'8-connect'}
    view = [(int, (0,1000), 0, 'torlorance', 'tor','value'),
            (list, ['4-connect', '8-connect'], str, 'fill', 'con', 'pix')]
        
    def mouse_down(self, ips, x, y, btn, **key):
        ips.snapshot()
        msk = floodfill(ips.img, x, y, self.para['tor'], self.para['con']=='8-connect')
        #plt.imshow(msk)
        #plt.show()
        color = ColorManager.get_front()
        if ips.get_nchannels()==1:color = np.mean(color)
        ips.img[msk] = color
        ips.update = 'pix'
    
    def mouse_up(self, ips, x, y, btn, **key):
        pass
    
    def mouse_move(self, ips, x, y, btn, **key):
        pass
        
    def mouse_wheel(self, ips, x, y, d, **key):
        pass

