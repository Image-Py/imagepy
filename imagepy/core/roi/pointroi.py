# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 22:35:55 2016
@author: yxl
"""
import wx
from ..draw import paint
from .roi import ROI
from ..manager import RoiManager
from imagepy import IPy

class PointRoi(ROI):
    dtype = 'point'
    def __init__(self, body=None):
        self.body = body if body!=None else []
        self.update = body!=[]
        self.infoupdate = body!=[]
        
    def add(self, p):
        self.body.append(p)
        self.update, self.infoupdate = True, True
    
    def snap(self, x, y, lim):
        cur, minl = None, 1e8
        for i in self.body:
            d = (i[0]-x)**2+(i[1]-y)**2
            if d < minl:cur,minl = i,d
        if minl**0.5>lim:return None
        return self.body.index(cur)
        
    def pick(self, x, y, lim):
        return self.snap(x, y, lim)
        
    def draged(self, ox, oy, nx, ny, i):
        self.body[i] = (nx, ny)
        self.update = False
        
    def countbox(self):
        self.box = [1000,1000,-1000,-1000]
        for x, y in self.body:
            if x<self.box[0]:self.box[0]=x
            if x>self.box[2]:self.box[2]=x
            if y<self.box[1]:self.box[1]=y
            if y>self.box[3]:self.box[3]=y
        
    def get_box(self):
        if self.infoupdate:
            self.countbox()
            self.infoupdate=False
        return self.box
        
    def info(self, ips, cur):
        k, u = ips.unit
        if cur==None:return
        x, y = self.body[cur]
        IPy.set_info('points:%.0f x:%.1f y:%.1f'%(len(self.body), x*k, y*k))

    '''
    def affine(self, m, o):
        plg = PointRoi()
        plg.body = affine(self.body, m, o)
        plg.update = True
        plg.infoupdate = True
        return plg
    '''
        
    def draw(self, dc, f):
        dc.SetPen(wx.Pen(RoiManager.get_color(), width=RoiManager.get_lw(), style=wx.SOLID))
        for i in self.body:
            dc.DrawCircle(f(*i), 2)
                
    def sketch(self, img, w=1, color=None):
        pen = paint.Paint()
        for i in self.body:
            pen.draw_point(img, i[0], i[1], w, color)
            
    def fill(self, img, color=None):
        self.sketch(img, 1, color)
        
if __name__ == '__main__':
    seq = [(0,0),(1,0),(0,1),(1,1),(0,0)]
    p = Polygon(seq)
    mp = toSegment(seq)