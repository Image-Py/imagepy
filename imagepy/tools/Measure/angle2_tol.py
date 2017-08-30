# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 22:21:32 2017

@author: yxl
"""

import wx
from imagepy.core.engine import Tool
import numpy as np
from numpy.linalg import norm
from .setting import Setting
from imagepy import IPy

class Angle:
    """Define the class with line drawing fucntions """
    dtype = 'angle'
    def __init__(self, body=None):
        self.body = body if body!=None else []
        self.buf = []
        
    def addline(self):
        line = self.buf
        if len(line)!=2 or line[0] !=line[-1]:
            self.body.append(line)
        self.buf = []
    
    def snap(self, x, y, lim):
        minl, idx = 1000, None
        for i in self.body:
            for j in i:
                d = (j[0]-x)**2+(j[1]-y)**2
                if d < minl:minl,idx = d,(i, i.index(j))
        return idx if minl**0.5<lim else None
        
    def pick(self, x, y, lim):
        return self.snap(x, y, lim)

    def draged(self, ox, oy, nx, ny, i):
        i[0][i[1]] = (nx, ny)
        
    def draw(self, dc, f, **key):
        dc.SetPen(wx.Pen(Setting['color'], width=1, style=wx.SOLID))
        dc.SetTextForeground(Setting['tcolor'])
        linefont = wx.Font(10, wx.FONTFAMILY_DEFAULT, 
                       wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False)
        dc.SetFont(linefont)
        dc.DrawLines([f(*i) for i in self.buf])
        for i in self.buf:dc.DrawCircle(f(*i),2)
        for line in self.body:
            dc.DrawLines([f(*i) for i in line])
            for i in line:dc.DrawCircle(f(*i),2)
            pts = np.array(line)
            mid = (pts[:-1]+pts[1:])/2

            dxy = (pts[:-1]-pts[1:])
            dxy[:,1][dxy[:,1]==0] = 1
            l = norm(dxy, axis=1)*-np.sign(dxy[:,1])
            ang = np.arccos(dxy[:,0]/l)/np.pi*180
            for i,j in zip(ang, mid):
                dc.DrawText('%.0f'%i, f(*j))

    def report(self, title):
        rst, titles = [], ['K']
        for line in self.body:
            pts = np.array(line)
            mid = (pts[:-1]+pts[1:])/2

            dxy = (pts[:-1]-pts[1:])
            dxy[:,1][dxy[:,1]==0] = 1
            l = norm(dxy, axis=1)*-np.sign(dxy[:,1])
            rst.append(np.round(np.arccos(dxy[:,0]/l)/np.pi*180,1))
        IPy.table(title, rst, titles)

class Plugin(Tool):
    """Define a class with some events callback fucntions """
    title = 'Angle2'
    def __init__(self):
        self.curobj = None
        self.doing = False
        self.odx,self.ody = 0, 0
            
    def mouse_down(self, ips, x, y, btn, **key):
        if key['ctrl'] and key['alt']:
            if isinstance(ips.mark, Angle):
                ips.mark.report(ips.title)
            return
        lim = 5.0/key['canvas'].get_scale()
        if btn==1:
            # If not painting and exists roi, then try to select roi?
            if not self.doing:
                if isinstance(ips.mark, Angle):
                    self.curobj = ips.mark.pick(x, y, lim)
                if self.curobj!=None:
                    return                    
                if not isinstance(ips.mark, Angle):
                    ips.mark = Angle()
                    self.doing = True
                elif key['shift']:
                    self.doing = True
                else: ips.mark = None
            if self.doing:
                ips.mark.buf.append((x,y))
                ips.mark.buf.append((x,y))
                self.curobj = (ips.mark.buf, -1)
                self.odx, self.ody = x,y

        ips.update = True
    
    def mouse_up(self, ips, x, y, btn, **key):
        self.curobj = None
        if self.doing:
            ips.mark.addline()
        self.doing = False
        ips.update = True
    
    def mouse_move(self, ips, x, y, btn, **key):
        if not isinstance(ips.mark, Angle):return
        lim = 5.0/key['canvas'].get_scale()      
        if btn==None:
            self.cursor = wx.CURSOR_CROSS
            if ips.mark.snap(x, y, lim)!=None:
                self.cursor = wx.CURSOR_HAND
        elif btn==1:
            ips.mark.draged(self.odx, self.ody, x, y, self.curobj)
            ips.update = True
        self.odx, self.ody = x, y
        
    def mouse_wheel(self, ips, x, y, d, **key):
        pass