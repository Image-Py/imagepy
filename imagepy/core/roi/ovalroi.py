# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 21:29:59 2016
@author: yxl
"""
import wx
import numpy as np
from ..draw import paint
from .roi import ROI
from .polygonroi import PolygonRoi
from ..manager import RoiManager
from imagepy import IPy

class OvalRoi(ROI):
    dtype = 'rect'
    def __init__(self, l=0, t=0, r=0, b=0):
        self.body = []
        self.update = False
        self.lt, self.tp, self.rt, self.bm = l, t, r, b
        self.commit()
    
    def snap(self, x, y, z, lim):
        if abs(x-self.lt)<lim and abs(y-(self.tp+self.bm)/2)<lim:return 'l'
        if abs(x-self.rt)<lim and abs(y-(self.tp+self.bm)/2)<lim:return 'r'
        if abs(x-(self.lt+self.rt)/2)<lim and abs(y-self.tp)<lim:return 't'
        if abs(x-(self.lt+self.rt)/2)<lim and abs(y-self.bm)<lim:return 'b'
        if abs(x-self.lt)<lim and abs(y-self.tp)<lim:return 'lt'
        if abs(x-self.rt)<lim and abs(y-self.bm)<lim:return 'rb'
        if abs(x-self.rt)<lim and abs(y-self.tp)<lim:return 'rt'
        if abs(x-self.lt)<lim and abs(y-self.bm)<lim:return 'lb'
        return None
    
    def commit(self):
        l,r,t,b = self.lt, self.rt, self.tp, self.bm
        self.update = True
        if l==r or t==b: 
            self.body = [];return False
        else: 
            ar = np.linspace(0, np.pi*2,29)
            xs = np.cos(ar)*abs(r-l)/2+(r+l)/2
            ys = np.sin(ar)*abs(t-b)/2+(t+b)/2
            self.body = [(x,y) for x,y in zip(xs,ys)]
            return True
        
    def pick(self, x, y, z, lim):
        rst = self.snap(x,y,z,lim)
        if rst != None:return rst
        if (x-self.lt)*(x-self.rt)<0 and (y-self.tp)*(y-self.bm)<0:
            return True
        return None

    def draged(self, ox, oy, nx, ny, nz, i):
        if i == True:
            self.lt, self.rt = self.lt+nx-ox, self.rt+nx-ox
            self.tp, self.bm = self.tp+ny-oy, self.bm+ny-oy
        else:
            if 'l' in i:self.lt = nx
            if 'r' in i:self.rt = nx
            if 't' in i:self.tp = ny
            if 'b' in i:self.bm = ny
        self.commit()
        
    def info(self, ips, cur):
        k, u = ips.unit
        l,r,t,b = self.lt, self.rt, self.tp, self.bm
        IPy.set_info('Rectangle : x:%.1f y:%.1f w:%.1f h:%.1f   S:%.1f'%(
            min(l,r)*k,min(t,b)*k,abs(r-l)*k,abs(b-t)*k,abs((r-l)*(b-t)/4*np.pi*k**2)))
    
    def get_box(self):
        return [self.lt, self.tp, self.rt, self.bm]
        
    def topolygon(self):
        pg = PolygonRoi()
        pg.body.append([self.body, []])
        return pg
    '''
    def affine(self, m, o):
        return self.topolygon().affine(m,o)
    '''
        
    def draw(self, dc, f, **key):
        dc.SetPen(wx.Pen(RoiManager.get_color(), width=RoiManager.get_lw(), style=wx.SOLID))
        if len(self.body)>1:
            dc.DrawLines([f(*i) for i in self.body])
        for i in [self.lt, (self.lt+self.rt)/2, self.rt]:
            for j in [self.tp, (self.tp+self.bm)/2, self.bm]:
                dc.DrawCircle(f(i,j),2)
                
    def sketch(self, img, w=1, color=None):
        pen = paint.Paint()
        xs, ys = [x[0] for x in self.body], [x[1] for x in self.body]
        pen.draw_path(img, xs, ys, w, color)
            
    def fill(self, img, color=None):
        pen = paint.Paint()
        pen.fill_polygon(self.body, img, [], color)