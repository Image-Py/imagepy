# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 15:55:42 2016

@author: yxl
"""
from core.engines import Filter
from core.managers import ColorManager

class Plugin(Filter):
    title = 'Fill'
    note = ['req_roi', 'all', 'auto_snap', 'not_channel']

    #process
    def run(self, ips, img, buf, para=None):
        buf[ips.get_msk()] = ColorManager.get_front(img.ndim==2)