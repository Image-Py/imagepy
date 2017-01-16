# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 22:35:55 2016

@author: yxl
"""
import wx
from core.draw import paint
from roi import ROI, affine

class PointRoi(ROI):
    dtype = 'point'
    def __init__(self, body=[]):
        self.body = body
        self.update = body!=[]
        self.infoupdate = body!=[]
        
    def add(self, p):
        self.body.append(p)
        self.update, self.infoupdate = True, True
    
    def snap(self, x, y):
        cur, minl = None, 1000
        for i in self.body:
            d = (i[0]-x)**2+(i[1]-y)**2
            if d < minl:cur,minl = i,d
        if minl>9:return None
        return self.body.index(cur)
        
    def pick(self, x, y):
        return self.snap(x, y)
        
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
        
    def affine(self, m, o):
        plg = PointRoi()
        plg.body = affine(self.body, m, o)
        plg.update = True
        plg.infoupdate = True
        return plg
        
    def draw(self, dc, f):
        dc.SetPen(wx.Pen((255,255,255), width=1, style=wx.SOLID))
        for i in self.body:
            dc.DrawCirclePoint(f(*i), 2)
                
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