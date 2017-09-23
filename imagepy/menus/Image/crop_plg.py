# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 02:32:31 2016
@author: yxl
"""

from imagepy.core.engine import Simple
import numpy as np

class Plugin(Simple):
    title = 'Crop'
    note = ['all', 'req_roi']

    def run(self, ips, imgs, para = None):
        sc, sr = ips.get_rect()
        if ips.is3d:
            imgs = imgs[:, sc, sr].copy()
        else:
            imgs = [i[sc,sr].copy() for i in imgs]
        ips.set_imgs(imgs)
        if not ips.backimg is None:
            ips.backimg = ips.backimg[sc, sr]
        ips.roi = ips.roi.affine(np.eye(2), (-sr.start, -sc.start))