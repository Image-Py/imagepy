# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 03:51:45 2016

@author: yxl
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 23:10:57 2016

@author: yxl
"""

import wx
import numpy as np
from core.engines import Tool
import scipy.ndimage as nimg

class Plugin(Tool):
    title = 'Scale'
    para = {'kx': 1, 'ky':1, 'ox':0, 'oy':0, 'img':True, 'msk':False}
    view = [(float, (-100,100), 3, 'KX', 'kx', ''),
            (float, (-100,100), 3, 'KY', 'ky', ''),
            (int, (-10000,10000), 0, 'OffX', 'ox', 'pix'),
            (int, (-10000,10000), 0, 'OffY', 'oy', 'pix'),
            (bool, 'scale image', 'img'),
            (bool, 'scale mask', 'msk')]
            
    def __init__(self):
        self.lt, self.tp, self.rt, self.bm = 0, 0, 0, 0
        self.going = False
        self.moving = False

        
    def draw(self, dc, f):
        body = [(self.lt,self.bm),(self.rt,self.bm),
                (self.rt,self.tp),(self.lt,self.tp),(self.lt,self.bm)]
        dc.SetPen(wx.Pen((0,255,0), width=1, style=wx.SOLID))
        dc.DrawLines([f(*i) for i in body])
        for i in body:dc.DrawCirclePoint(f(*i),2)
        dc.DrawCirclePoint(f(self.lt, (self.tp+self.bm)/2),2)
        dc.DrawCirclePoint(f(self.rt, (self.tp+self.bm)/2),2)
        dc.DrawCirclePoint(f((self.lt+self.rt)/2, self.tp),2)
        dc.DrawCirclePoint(f((self.lt+self.rt)/2, self.bm),2)
            
    def snap(self, x, y):
        if abs(x-self.lt)<3 and abs(y-(self.tp+self.bm)/2)<3:return 'l'
        if abs(x-self.rt)<3 and abs(y-(self.tp+self.bm)/2)<3:return 'r'
        if abs(x-(self.lt+self.rt)/2)<3 and abs(y-self.tp)<3:return 't'
        if abs(x-(self.lt+self.rt)/2)<3 and abs(y-self.bm)<3:return 'b'
        if abs(x-self.lt)<3 and abs(y-self.tp)<3:return 'lt'
        if abs(x-self.rt)<3 and abs(y-self.bm)<3:return 'rb'
        if abs(x-self.rt)<3 and abs(y-self.tp)<3:return 'rt'
        if abs(x-self.lt)<3 and abs(y-self.bm)<3:return 'lb'
        if (x-self.lt)*(x-self.rt)<0 and (y-self.tp)*(y-self.bm)<0:
            self.ox, self.oy = x, y
            return True
        return False
        
    def mouse_down(self, ips, x, y, btn, **key):    
        if self.going == False:
            self.going = True
            self.show(ips)
        elif self.going:
            self.moving = self.snap(x, y)
        
    def mouse_up(self, ips, x, y, btn, **key):
        if not self.going : return
        else:
            self.run(ips, ips.snap, ips.get_img(), self.para)
        
    def count(self, dir=True):
        if dir:
            self.para['ox'] = int((self.lt+self.rt)/2)
            self.para['oy'] = int((self.tp+self.bm)/2)
            self.para['kx'] = (self.rt-self.lt)*1.0/self.oriw
            self.para['ky'] = (self.tp-self.bm)*1.0/self.orih
        else:
            self.lt = self.para['ox']-self.oriw*self.para['kx']/2
            self.rt = self.para['ox']+self.oriw*self.para['kx']/2
            self.bm = self.para['oy']-self.orih*self.para['ky']/2
            self.tp = self.para['oy']+self.orih*self.para['ky']/2
        
    def mouse_move(self, ips, x, y, btn, **key):
        if not self.going : return
        if btn==None:
            self.cursor = wx.CURSOR_CROSS
            if isinstance(self.snap(x, y), str):
                self.cursor = wx.CURSOR_HAND
        elif self.moving==True:
            self.lt+=x-self.ox
            self.rt+=x-self.ox
            self.bm+=y-self.oy
            self.tp+=y-self.oy
            self.ox, self.oy = x, y
            self.count()
            self.dialog.reset()
            ips.update = True
        elif self.moving != False:
            if 'l' in self.moving:self.lt = x
            if 'r' in self.moving:self.rt = x
            if 't' in self.moving:self.tp = y
            if 'b' in self.moving:self.bm = y
            self.count()
            self.dialog.reset()
            ips.update = True
        
    def on_load(self, ips):
        self.bufroi = ips.roi
        ips.snapshot()
        
        self.lt, self.tp, self.rt, self.bm = 0, 0, ips.size[1], ips.size[0]
        
        if ips.roi!=None:
            box = ips.roi.get_box()
            if box[0]!=box[2] and box[1]!=box[3]:
                self.lt, self.tp, self.rt, self.bm = box

        self.orio = ((self.lt+self.rt)/2,(self.tp+self.bm)/2)
        self.oriw, self.orih = self.rt - self.lt, self.tp - self.bm

        self.para['ox'] = (self.lt+self.rt)/2
        self.para['oy'] = (self.tp+self.bm)/2
        self.para['kx'] = self.para['ky'] = 1

        ips.mark = self
        ips.update = True

    def on_ok(self, ips):
        self.ips.mark = None 
        self.going = False
        self.run(ips, ips.snap, ips.get_img(), self.para)
        
    def on_cancel(self, ips):
        self.ips.mark = None
        self.ips.reset()
        ips.roi = self.bufroi
        ips.update = True
        self.going = False
        
    def run(self, ips, img, buf, para = None):
        if para == None: para = self.para
        self.count(False)
        trans = np.array([[1/self.para['ky'],0],[0,1/self.para['kx']]])
        o = np.array([self.para['oy'], self.para['ox']])
        offset = self.orio[::-1]-trans.dot(o)
        if self.para['img']:
            if ips.chanels==1:
                nimg.affine_transform(img, trans, output=buf, offset=offset)
            else:
                for i in range(ips.chanels):
                    nimg.affine_transform(img[:,:,i], trans, output=buf[:,:,i], offset=offset)
        
        trans = np.array([[self.para['kx'],0],[0, self.para['ky']]])
        offset = o[::-1]-trans.dot(self.orio)
        if self.para['msk'] and self.bufroi!=None:ips.roi = self.bufroi.affine(trans, offset)
        if self.para['img'] and ips.get_msk('out')!=None: 
            buf[ips.get_msk('out')] = img[ips.get_msk('out')]
        ips.update = True