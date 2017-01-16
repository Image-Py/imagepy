# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 15:55:42 2016

@author: yxl
"""

from core.engines import Filter
from core.managers import ColorManager

class Plugin(Filter):
    title = 'Sketch'
    note = ['req_roi', 'all', 'auto_snap', 'not_channel']
    
    #parameter
    para = {'width':1}
    view = [(int, (0,30), 0,  u'width', 'width', 'pix')]

    #process
    def run(self, ips, img, buf, para = None):
        buf[ips.get_msk(para['width'])] = ColorManager.get_front(img.ndim==2)