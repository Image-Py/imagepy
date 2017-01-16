# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 15:55:42 2016

@author: yxl
"""

from core.engines import Simple
from core.roi.rectangleroi import RectangleRoi
from core.managers import ClipBoardManager
import numpy as np

class Plugin(Simple):
    title = 'Copy'
    note = ['all']
    
    #process
    def run(self, ips, imgs, para = None):
        if ips.roi == None:
            ClipBoardManager.img = ips.get_subimg().copy()
            ClipBoardManager.roi = RectangleRoi(0, 0, ips.size[1], ips.size[0])
        else:
            box = ips.roi.get_box()
            ClipBoardManager.img = ips.get_subimg().copy()
            ClipBoardManager.roi = ips.roi.affine(np.eye(2), (-box[0], -box[1]))
            