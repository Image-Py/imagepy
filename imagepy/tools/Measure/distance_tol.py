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

class Distance:
    """Define the distance class"""
    dtype = 'distance'
    def __init__(self, body=None, unit=None):
        self.body = body if body!=None else []
        self.buf, self.unit = [], unit
        
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
        font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False)
        dc.SetFont(font)
        dc.DrawLines([f(*i) for i in self.buf])
        for i in self.buf:dc.DrawCircle(f(*i),2)
        for line in self.body:
            dc.DrawLines([f(*i) for i in line])
            for i in line:dc.DrawCircle(f(*i),2)
            pts = np.array(line)
            mid = (pts[:-1]+pts[1:])/2

            dis = norm((pts[:-1]-pts[1:]), axis=1)
            unit = 1 if self.unit is None else self.unit[0]
            for i,j in zip(dis, mid):
                dc.DrawText('%.2f'%(i*unit), f(*j))

    def report(self, title):
        rst = []
        for line in self.body:
            pts = np.array(line)
            dis = norm((pts[:-1]-pts[1:]), axis=1)
            dis *= 1 if self.unit is None else self.unit[0]
            rst.append(list(dis.round(2)))
        lens = [len(i) for i in rst]
        maxlen = max(lens)
        fill = [[0]*(maxlen-i) for i in lens]
        rst = [i+j for i,j in zip(rst, fill)]
        titles = ['L{}'.format(i+1) for i in range(maxlen)]
        IPy.table(title, rst, titles)

class Plugin(Tool):
    """Define the diatance class plugin with the event callback functions"""
    title = 'Distance'
    def __init__(self):
        self.curobj = None
        self.doing = False
        self.odx,self.ody = 0, 0
            
    def mouse_down(self, ips, x, y, btn, **key):
        if key['ctrl'] and key['alt']:
            if isinstance(ips.mark, Distance):
                ips.mark.report(ips.title)
            return

        lim = 5.0/key['canvas'].get_scale()
        if btn==1:
            if not self.doing:
                if isinstance(ips.mark, Distance):
                    self.curobj = ips.mark.pick(x, y, lim)
                if self.curobj!=None:return
                    
                if not isinstance(ips.mark, Distance):
                    ips.mark = Distance(unit=ips.unit)
                    self.doing = True
                elif key['shift']:
                    self.doing = True
                else: ips.mark = None
            if self.doing:
                ips.mark.buf.append((x,y))
                self.curobj = (ips.mark.buf, -1)
                self.odx, self.ody = x,y
            
        elif btn==3:
            if self.doing:
                ips.mark.buf.append((x,y))
                self.doing = False
                ips.mark.addline()
        ips.update = True
    
    def mouse_up(self, ips, x, y, btn, **key):
        self.curobj = None
    
    def mouse_move(self, ips, x, y, btn, **key):
        if not isinstance(ips.mark, Distance):return
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