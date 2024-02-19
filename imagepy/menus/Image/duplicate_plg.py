# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 19:47:34 2016
@author: yxl
"""

from sciapp.action import Simple
from sciapp.object import Image, ROI
from sciapp.util import offset, mark2shp
import numpy as np

class Duplicate(Simple):
    title = 'Duplicate'
    note = ['all']
    
    def load(self, ips):
        if ips.slices > 1:
            self.para = {'stack':True}
            self.view = [(bool, 'stack', 'duplicate stack')]
        else: 
            self.para = {'stack':True}
            self.view = None
        return True

    def run(self, ips, imgs, para = None):
        if not para['stack']: imgs = [ips.img]
        sli = ips.rect
        imgs = [i[sli].copy() for i in imgs]
        if ips.isarray: imgs = np.array(imgs)
        new = Image(imgs, ips.name + '-duplicate')
        if not ips.roi is None:
            new.roi = ROI(mark2shp(ips.roi.to_mark()))
            offset(new.roi, new.roi.box[0]*-1, new.roi.box[1]*-1)
            new.roi.dirty = True
        if not ips.back is None and not ips.back.imgs is None:
            back = [i[sli].copy() for i in ips.back.imgs]
            if ips.isarray: back = np.array(back)
            back = Image(back, ips.back.name+'-duplicate')
            back.cn, back.rg, back.mode = ips.back.cn, ips.back.rg, ips.back.mode
            new.back, new.mode = back, ips.mode
            self.app.show_img(back)
        self.app.show_img(new)

class Crop(Simple):
    title = 'Crop'
    note = ['all', 'req_roi']

    def run(self, ips, imgs, para = None):
        sc, sr = ips.rect
        if ips.isarray: imgs = imgs[:, sc, sr].copy()
        else: imgs = [i[sc,sr].copy() for i in imgs]
        ips.set_imgs(imgs)
        if not ips.back is None:
            if ips.back.isarray: imgs = ips.back.imgs[:, sc, sr].copy()
            else: imgs = [i[sc,sr].copy() for i in ips.back.imgs]
            ips.back.set_imgs(imgs)
        offset(ips.roi, ips.roi.box[0]*-1, ips.roi.box[1]*-1)

class Rename(Simple):
    title = 'Rename'
    note = ['all']
    
    para = {'name':'Undefined'}
    view = [(str, 'name', 'name', '')]
    #process
    def run(self, ips, imgs, para = None):
        win = self.app.wimg_manager.get(ips.name)
        self.app.img_manager.remove(ips.name)
        self.app.wimg_manager.remove(ips.name)
        ips.name = self.app.img_manager.name(para['name'])
        self.app.img_manager.add(ips.name, ips)
        self.app.wimg_manager.add(ips.name, win)

plgs = [Rename, Duplicate, Crop]