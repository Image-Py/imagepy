# -*- coding: utf-8 -*-
"""
Created on Sun Dec 18 22:31:12 2016

@author: yxl
"""
from core.managers import RoiManager
from core.engines import Simple
from core.roi.rectangleroi import RectangleRoi
import IPy

class SelectAll(Simple):
    title = 'Select All'
    note = ['all']

    def run(self, ips, imgs, para = None):
        ips.roi = RectangleRoi(0,0,ips.size[1],ips.size[0])

class SelectNone(Simple):
    title = 'Select None'
    note = ['all']

    def run(self, ips, imgs, para = None):
        ips.roi = None
        
class Add2Manager(Simple):
    title = 'Add To Manager'
    note = ['all', 'req_roi']
    para = {'name':''}
    view = [(str, 'Name', 'name', '')]

    def run(self, ips, imgs, para = None):
        RoiManager.add(para['name'], ips.roi)
        
class LoadRoi(Simple):
    title = 'Load Roi'
    note = ['all']
    para = {'name':''}
    
    def load(self, ips):
        titles = RoiManager.rois.keys()
        if len(titles)==0: 
            IPy.alert('No roi in manager!')
            return False
        self.para['name'] = titles[0]
        LoadRoi.view = [(list, titles, str, 'Name', 'name', '')]
        return True

    def run(self, ips, imgs, para = None):
        ips.roi = RoiManager.get(para['name'])
        
class Inflate(Simple):
    title = 'Inflate'
    note = ['all', 'req_roi']
    para = {'r':5}
    view = [(int, (1,100),0, 'radius', 'r','pix')]

    def run(self, ips, imgs, para = None):
        ips.roi = ips.roi.buffer(para['r'])
        
class Shrink(Simple):
    title = 'Shrink'
    note = ['all', 'req_roi']
    para = {'r':5}
    view = [(int, (1,100),0, 'radius', 'r','pix')]

    def run(self, ips, imgs, para = None):
        ips.roi = ips.roi.buffer(-para['r'])
        
class Convex(Simple):
    title = 'Convex Hull'
    note = ['all', 'req_roi']
    
    def run(self, ips, imgs, para = None):
        ips.roi = ips.roi.convex()
        
class Box(Simple):
    title = 'Bound Box'
    note = ['all', 'req_roi']
    
    def run(self, ips, imgs, para = None):
        ips.roi = ips.roi.bounds()
        
class Clip(Simple):
    title = 'Clip Roi'
    note = ['all', 'req_roi']
    
    def run(self, ips, imgs, para = None):
        rect = RectangleRoi(0,0,ips.size[1],ips.size[0])
        ips.roi = ips.roi.clip(rect)
        
class Invert(Simple):
    title = 'Invert Roi'
    note = ['all', 'req_roi']
    
    def run(self, ips, imgs, para = None):
        rect = RectangleRoi(0,0,ips.size[1],ips.size[0])
        ips.roi = ips.roi.invert(rect)
        
plgs = [SelectAll, SelectNone, '-', Inflate, Shrink, Convex, Box, Clip, Invert, '-', Add2Manager, LoadRoi]