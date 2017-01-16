# -*- coding: utf-8 -*-
"""
Created on Sat Nov 26 01:26:25 2016

@author: yxl
"""
from core.pixcel import bliter
from core.engines import Simple, Tool
import numpy as np
from core.managers import ClipBoardManager

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
    
class Plugin(Simple):
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
        