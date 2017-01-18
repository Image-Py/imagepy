# -*- coding: utf-8 -*-
"""
Created on Sat Nov 26 01:26:25 2016

@author: yxl
"""
from core.pixcel import bliter
from core.engines import Simple, Tool, Filter
import numpy as np
from core.managers import ClipBoardManager, ColorManager
from core.roi.rectangleroi import RectangleRoi

class PasteMove(Tool):
    def __init__(self):
        self.moving = True
        self.cx, self.cy = 0, 0
        
    def mouse_down(self, ips, x, y, btn, **key):    
        goon = ips.roi.pick(x, y)
        if goon != True : 
            print 'end'
        else :
            self.moving = True
            self.ox, self.oy = x, y
        
    def mouse_up(self, ips, x, y, btn, **key):
        if self.moving == True:
            self.moving = False
            ci = ClipBoardManager.img
            img = ips.get_img()
            #ips.roi.draged(ci.shape[1]/2,ci.shape[0]/2, ips.size[1]/2, ips.size[0]/2, True)
            #ips.roi = IPy.clipboard[1].affine(np.eye(2), ((np.array(ips.size)-ci.shape[:2])[::-1]/2))          
            x,y = (np.array(ips.size)-ci.shape[:2])/2+(self.cy,self.cx)
            bliter.blit(img, ci, y, x)
                        
            ips.reset(True)
            ips.update = True
        
    def mouse_move(self, ips, x, y, btn, **key):
        if self.moving==True and btn!=None:
            ips.roi.draged(self.ox, self.oy, x, y, True)
            self.cx += x-self.ox
            self.cy += y-self.oy
            self.ox, self.oy = x, y
            ips.update = True
    
class Paste(Simple):
    title = 'Paste'
    note = ['all']
    
    #process
    def run(self, ips, imgs, para = None):
        if ClipBoardManager.img == None:return
        ips.snapshot()
        ips.roi = ClipBoardManager.roi
        ci = ClipBoardManager.img
        img = ips.get_img()
        #ips.roi.draged(ci.shape[1]/2,ci.shape[0]/2, ips.size[1]/2, ips.size[0]/2, True)
        ips.roi = ClipBoardManager.roi.affine(np.eye(2), ((np.array(ips.size)-ci.shape[:2])[::-1]/2))          
        x,y = (np.array(ips.size)-ci.shape[:2])/2
        bliter.blit(img, ci, y, x)
        ips.reset(True)
        ips.tool = PasteMove()
        #nimg.affine_transform(img, np.eye(2), output=buf, offset=()
        
class Clear(Filter):
    title = 'Clear'
    note = ['req_roi', 'all', 'auto_snap', 'not_channel']

    #process
    def run(self, ips, img, buf, para=None):
        buf[ips.get_msk()] = ColorManager.get_back(img.ndim==2)
        
class ClearOut(Filter):
    title = 'Clear Out'
    note = ['req_roi', 'all', 'auto_snap', 'not_channel']

    #process
    def run(self, ips, img, buf, para=None):
        buf[ips.get_msk('out')] = ColorManager.get_back(img.ndim==2)
        
class Copy(Simple):
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
            
class Sketch(Filter):
    title = 'Sketch'
    note = ['req_roi', 'all', 'auto_snap', 'not_channel']
    
    #parameter
    para = {'width':1}
    view = [(int, (0,30), 0,  u'width', 'width', 'pix')]

    #process
    def run(self, ips, img, buf, para = None):
        buf[ips.get_msk(para['width'])] = ColorManager.get_front(img.ndim==2)
        
class Fill(Filter):
    title = 'Fill'
    note = ['req_roi', 'all', 'auto_snap', 'not_channel']

    #process
    def run(self, ips, img, buf, para=None):
        buf[ips.get_msk()] = ColorManager.get_front(img.ndim==2)
        
class Undo(Simple):
    title = 'Undo'
    note = ['all']
    #process
    def run(self, ips, img, buf, para=None):
        ips.swap()
        
plgs = [Undo, '-', Copy, Paste, Sketch, Fill, '-', Clear, ClearOut]