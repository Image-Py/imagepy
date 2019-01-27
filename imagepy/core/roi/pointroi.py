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
import numpy as np

class PointRoi(ROI):
    dtype = 'point'
    def __init__(self, body=None):
        self.body = body if body!=None else []
        self.body = [i if len(i)==3 else tuple(i) + (0,) for i in self.body]
        self.update = body!=[]
        self.infoupdate = body!=[]
        
    def add(self, p):
        self.body.append(p)
        self.update, self.infoupdate = True, True
    
    def snap(self, x, y, z, lim):
        cur, minl = None, 1e8
        for i in self.body:
            if z!=i[2]:continue
            d = (i[0]-x)**2+(i[1]-y)**2
            if d < minl:cur,minl = i,d
        if minl**0.5>lim:return None
        return self.body.index(cur)
        
    def pick(self, x, y, z, lim):
        return self.snap(x, y, z, lim)
        
    def draged(self, ox, oy, nx, ny, nz, i):
        self.body[i] = (nx, ny, nz)
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
        x, y, z = self.body[cur]
        IPy.set_info('points:%.0f x:%.1f y:%.1f z:%.1f'%(len(self.body), x*k, y*k, z*k))
        
    def draw(self, dc, f, **key):



        colormap = (tuple(np.array(RoiManager.get_color())//2), RoiManager.get_color())
        font = wx.Font(8, wx.FONTFAMILY_DEFAULT, 
                       wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False)
        
        dc.SetFont(font)
        for c,r,z in self.body:
            pos = f(*(c,r))
            dc.SetPen(wx.Pen(colormap[z==key['cur']], width=RoiManager.get_lw(), style=wx.SOLID))
            dc.SetTextForeground(colormap[z==key['cur']])
            dc.DrawCircle(pos[0], pos[1], 2)
            dc.DrawText('z={}'.format(z), pos[0], pos[1])
                
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