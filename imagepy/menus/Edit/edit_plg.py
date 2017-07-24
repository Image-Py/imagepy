# -*- coding: utf-8 -*-
"""
Created on Sat Nov 26 01:26:25 2016
@author: yxl
"""
import numpy as np
from imagepy.core.pixel import bliter
from imagepy.core.engine import Simple, Tool, Filter
from imagepy.core.roi.rectangleroi import RectangleRoi
from imagepy.core.manager import ClipBoardManager, ColorManager

class PasteMove(Tool):
    def __init__(self):
        self.moving = True
        self.cx, self.cy = 0, 0
        
    def mouse_down(self, ips, x, y, btn, **key):    
        goon = ips.roi.pick(x, y, 0)
        print(goon)
        if goon != True : 
            print('mouse_down')
        else :
            self.moving = True
            self.ox, self.oy = x, y
        
    def mouse_up(self, ips, x, y, btn, **key):
        if self.moving == True:
            self.moving = False
            ci = ClipBoardManager.img
            img = ips.img
            #ips.roi.draged(ci.shape[1]/2,ci.shape[0]/2, ips.size[1]/2, ips.size[0]/2, True)
            #ips.roi = IPy.clipboard[1].affine(np.eye(2), ((np.array(ips.size)-ci.shape[:2])[::-1]/2))          
            x,y = (np.array(ips.size)-ci.shape[:2])/2+(self.cy,self.cx)
            bliter.blit(img, ci, y, x)
                        
            ips.reset(True)
            ips.update = 'pix'
        
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
    
    def run(self, ips, imgs, para = None):
        if ClipBoardManager.img == None:return
        ips.snapshot()
        ips.roi = ClipBoardManager.roi
        ci = ClipBoardManager.img
        img = ips.img
        #ips.roi.draged(ci.shape[1]/2,ci.shape[0]/2, ips.size[1]/2, ips.size[0]/2, True)
        ips.roi = ClipBoardManager.roi.affine(np.eye(2), 
                                              ((np.array(ips.size)-ci.shape[:2])[::-1]/2))
        
        x,y = (np.array(ips.size)-ci.shape[:2])/2
        bliter.blit(img, ci, y, x)
        ips.reset(True)
        ips.tool = PasteMove()
        #nimg.affine_transform(img, np.eye(2), output=buf, offset=()
        
class Clear(Filter):
    title = 'Clear'
    note = ['req_roi', 'all', 'auto_snap', 'not_channel']

    def run(self, ips, snap, img, para=None):
        img[ips.get_msk()] = ColorManager.get_back(snap.ndim==2)
        
class ClearOut(Filter):
    title = 'Clear Out'
    note = ['req_roi', 'all', 'auto_snap', 'not_channel']

    def run(self, ips, snap, img, para=None):
        img[ips.get_msk('out')] = ColorManager.get_back(snap.ndim==2)
        
class Copy(Simple):
    title = 'Copy'
    note = ['all']
    
    def run(self, ips, imgs, para = None):
        if ips.roi == None:
            ClipBoardManager.img = ips.get_subimg().copy()
            ClipBoardManager.roi = RectangleRoi(0, 0, ips.size[1], ips.size[0])
        else:
            box = ips.roi.get_box()
            ClipBoardManager.img = ips.get_subimg().copy()
            ClipBoardManager.roi = ips.roi.affine(np.eye(2), (-box[0], -box[1]))
            
class Sketch(Filter):
    ## TODO: What is this?
    title = 'Sketch'
    note = ['req_roi', 'all', 'auto_snap', 'not_channel']
    para = {'width':1}
    view = [(int, (0,30), 0,  'width', 'width', 'pix')]

    def run(self, ips, snap, img, para = None):
        img[ips.get_msk(para['width'])] = ColorManager.get_front(snap.ndim==2)
        
class Fill(Filter):
    title = 'Fill'
    note = ['req_roi', 'all', 'auto_snap', 'not_channel']

    def run(self, ips, snap, img, para=None):
        img[ips.get_msk()] = ColorManager.get_front(snap.ndim==2)
        
class Undo(Simple):
    title = 'Undo'
    note = ['all']

    def run(self, ips, img, buf, para=None):
        ips.swap()
        
class Invert(Filter):
    title = 'Invert'
    note = ['all', 'auto_msk', 'auto_snap', 'preview']

    def run(self, ips, snap, img, para = None):
        np.subtract(ips.range[1], snap, out=img)
        
plgs = [Undo, '-', Copy, Paste, Sketch, Fill, Invert, '-', Clear, ClearOut]