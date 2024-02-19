# -*- coding: utf-8 -*-
"""
Created on Sat Nov 26 01:26:25 2016
@author: yxl
"""
import numpy as np
from sciapp.action import Simple, Filter
from sciapp.action import ImageTool

class PasteMove(ImageTool):
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
            ci = self.app.manager('xxxxxx')
            img = ips.img
            #ips.roi.draged(ci.shape[1]/2,ci.shape[0]/2, ips.size[1]/2, ips.size[0]/2, True)
            #ips.roi = IPy.clipboard[1].affine(np.eye(2), ((np.array(ips.size)-ci.shape[:2])[::-1]/2))          
            x,y = (np.array(ips.size)-ci.shape[:2])/2+(self.cy,self.cx)
            bliter.blit(img, ci, y, x)
                        
            ips.reset(True)
            ips.update()
        
    def mouse_move(self, ips, x, y, btn, **key):
        if self.moving==True and btn!=None:
            ips.roi.draged(self.ox, self.oy, x, y, True)
            self.cx += x-self.ox
            self.cy += y-self.oy
            self.ox, self.oy = x, y
            ips.update()
    
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
        color = self.app.manager('color').get('back')
        color = np.array([color]).ravel()
        if ips.channels != len(color): color = color.mean()
        img[ips.mask()] = color
        
class ClearOut(Filter):
    title = 'Clear Out'
    note = ['req_roi', 'all', 'auto_snap', 'not_channel']

    def run(self, ips, snap, img, para=None):
        color = self.app.manager('color').get('back')
        color = np.array([color]).ravel()
        if ips.channels != len(color): color = color.mean()
        img[ips.mask('out')] = color
        
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
    view = [(int, 'width', (0,30), 0,  'width', 'pix')]

    def run(self, ips, snap, img, para = None):
        color = self.app.manager('color').get('front')
        color = np.array([color]).ravel()
        if ips.channels != len(color): color = color.mean()
        img[ips.mask(para['width'])] = color
        
class Fill(Filter):
    title = 'Fill'
    note = ['req_roi', 'all', 'auto_snap', 'not_channel']

    def run(self, ips, snap, img, para=None):
        color = self.app.manager('color').get('front')
        color = np.array([color]).ravel()
        if ips.channels != len(color): color = color.mean()
        img[ips.mask()] = color
        
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