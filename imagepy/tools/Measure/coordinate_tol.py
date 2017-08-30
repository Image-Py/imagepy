# -*- coding: utf-8 -*-
"""
Created on Thu Feb  2 23:04:46 2017

@author: yxl
"""

import wx
from imagepy.core.engine import Tool
from .setting import Setting
from imagepy import IPy

class Coordinate:
    """Define the coordinate class"""
    dtype = 'coordinate'
    def __init__(self, body=None, unit=None):
        self.body = body if body!=None else []
        self.unit = unit
        
    def add(self, p):
        self.body.append(p)
    
    def snap(self, x, y, lim):
        cur, minl = None, 1000
        for i in self.body:
            d = (i[0]-x)**2+(i[1]-y)**2
            if d < minl:cur,minl = i,d
        if minl**0.5>lim:return None
        return self.body.index(cur)
        
    def pick(self, x, y, lim):
        return self.snap(x, y, lim)
        
    def draged(self, ox, oy, nx, ny, i):
        self.body[i] = (nx, ny)
        
    def draw(self, dc, f, **key):
        dc.SetPen(wx.Pen(Setting['color'], width=1, style=wx.SOLID))
        dc.SetTextForeground(Setting['tcolor'])
        font = wx.Font(10, wx.FONTFAMILY_DEFAULT, 
                       wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False)
        
        dc.SetFont(font)
        for i in self.body:
            x,y = f(*i)
            unit = 1 if self.unit is None else self.unit[0]
            dc.DrawCircle(x, y, 2)
            dc.DrawText('(%.1f,%.1f)'%(i[0]*unit, i[1]*unit), x, y)

    def report(self, title):
        unit = 1 if self.unit is None else self.unit[0]
        rst = [(x*unit, y*unit) for x,y in self.body]
        titles = ['OX', 'OY']
        IPy.table(title, rst, titles)

class Plugin(Tool):
    """Define the coordinate class plugin with the event callback functions"""
    title = 'Coordinate'
    def __init__(self):
        self.curobj = None
        self.odx, self.ody = 0, 0
            
    def mouse_down(self, ips, x, y, btn, **key):
        if key['ctrl'] and key['alt']:
            if isinstance(ips.mark, Coordinate):
                ips.mark.report(ips.title)
            return
        lim = 5.0/key['canvas'].get_scale() 
        if btn==1:
            if isinstance(ips.mark, Coordinate):
                self.curobj = ips.mark.pick(x, y, lim)
            if self.curobj!=None:return
            if not isinstance(ips.mark, Coordinate):
                ips.mark = Coordinate(unit=ips.unit)
            elif not key['shift']:
                ips.mark = Coordinate(unit=ips.unit)
            ips.mark.add((x,y))
            self.curobj = ips.mark.pick(x,y, lim)
            ips.update = True
            self.odx, self.ody = x, y
    
    def mouse_up(self, ips, x, y, btn, **key):
        self.curobj = None
    
    def mouse_move(self, ips, x, y, btn, **key):
        if not isinstance(ips.mark, Coordinate):return
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