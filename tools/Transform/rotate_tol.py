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
    title = 'Rotate'
    para = {'ang':0, 'ox':0, 'oy':0, 'img':True, 'msk':False}
    view = [(int, (0,360), 0, 'angle', 'ang', 'degree'),
            (int, (0,5000), 0, 'OX', 'ox', 'pix'),
            (int, (0,5000), 0, 'OY', 'oy', 'pix'),
            (bool, 'rotate image', 'img'),
            (bool, 'rotate mask', 'msk')]
            
    def __init__(self):
        self.going = False
        self.moving = False
        
    def draw(self, dc, f):
        dc.SetPen(wx.Pen((0,255,0), width=1, style=wx.SOLID))
        sox, soy = f(self.para['ox'], self.para['oy'])
        dc.DrawCirclePoint((sox, soy), 5)
        a = np.linspace(0, 2*np.pi, 20)
        dc.DrawLines(zip(sox+np.cos(a)*40, soy+np.sin(a)*40))
        a = self.para['ang']*np.pi/180
        dc.DrawCirclePoint((sox+np.cos(a)*40, soy+np.sin(a)*40), 3)
            
    def mouse_down(self, ips, x, y, btn, **key):        
        if self.going == False:
            self.going = True
            self.show(ips)
        elif self.going:
            if abs(x-self.para['ox'])<3 and abs(y-self.para['oy'])<3:
                self.moving = True
        
    def mouse_up(self, ips, x, y, btn, **key):
        if not self.going : return
        if self.moving:
            self.moving = False
        else:
            self.run(ips, ips.snap, ips.get_img(), self.para)
        
    def mouse_move(self, ips, x, y, btn, **key):
        if not self.going : return
        if btn==None:
            self.cursor = wx.CURSOR_CROSS
            if abs(x-self.para['ox'])<3 and abs(y-self.para['oy']<3):
                self.cursor = wx.CURSOR_HAND
        elif self.moving:
            self.para['ox'], self.para['oy'] = x, y
            self.dialog.reset()
            ips.update = True
        else:
            dx, dy = x-self.para['ox'], y-self.para['oy']
            ang = np.arccos(dx/np.sqrt(dx**2+dy**2))
            if dy<0: ang = np.pi*2-ang
            ang = int(ang/np.pi*180)
            self.para['ang'] = ang
            self.dialog.reset()
            ips.update = True
        
    def on_load(self, ips):
        self.bufroi = ips.roi
        ips.snapshot()
        self.para['ang'] = 0
        self.para['oy'], self.para['ox'] = np.array(ips.size)/2
        if ips.roi!=None:
            box = ips.roi.get_box()
            if box[0]!=box[2] and box[1]!=box[3]:
                self.para['oy'] = int((box[1]+box[3])/2)
                self.para['ox'] = int((box[0]+box[2])/2)
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
        a = para['ang']/180.0*np.pi
        trans = np.array([[np.cos(a),-np.sin(a)],[np.sin(a),np.cos(a)]])
        o = np.array([self.para['oy'], self.para['ox']])
        offset = o-trans.dot(o)
        if self.para['img']:
            if ips.chanels==1:
                nimg.affine_transform(img, trans, output=buf, offset=offset)
            else:
                for i in range(ips.chanels):
                    nimg.affine_transform(img[:,:,i], trans, output=buf[:,:,i], offset=offset)
        if self.para['msk'] and self.bufroi!=None:ips.roi = self.bufroi.affine(trans, o[::-1]-trans.dot(o[::-1]))
        if self.para['img'] and not ips.get_msk('out') is None: 
            buf[ips.get_msk('out')] = img[ips.get_msk('out')]
        ips.update = True
