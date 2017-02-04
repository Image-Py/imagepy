# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 17:35:09 2016

@author: yxl
"""
from core.roi import polygonroi
import wx

class Polygonbuf:
    def __init__(self):
        self.buf = [[],[]]
        
    def addpoint(self, p):
        self.buf[0].append(p)
        
    def draw(self, dc, f):
        dc.SetPen(wx.Pen((0,255,0), width=1, style=wx.SOLID))
        dc.DrawLines([f(*i) for i in self.buf[0]])
        for i in self.buf[0]: dc.DrawCirclePoint(f(*i),2)
    
    def pop(self):
        a = self.buf
        self.buf = [[],[]]
        return a
        
from core.engines import Tool

class Plugin(Tool):
    title = 'Polygon'
    def __init__(self):
        self.curobj = None
        self.doing = False
        self.oper = ''
        self.helper = Polygonbuf()
            
    def mouse_down(self, ips, x, y, btn, **key): 
        lim = 5.0/key['canvas'].get_scale() 
        ips.mark = self.helper
        if btn==1:
            if not self.doing:
                if ips.roi!= None:
                    self.curobj = ips.roi.pick(x, y, lim)
                if not self.curobj in (None,True):return
                self.oper = '+'
                if ips.roi == None:
                    ips.roi = polygonroi.PolygonRoi()
                    self.doing = True
                elif hasattr(ips.roi, 'topolygon'):
                    ips.roi = ips.roi.topolygon()
                    if key['shift']: self.oper,self.doing = '+',True
                    elif key['ctrl']: self.oper,self.doing = '-',True
                    elif self.curobj: return
                    else: ips.roi=None
                else: ips.roi = None
            if self.doing:
                self.helper.addpoint((x,y))
                self.curobj = (self.helper.buf[0], -1)
                self.odx, self.ody = x, y
                
        elif btn==3:
            if self.doing:
                self.helper.addpoint((x,y))
                self.doing = False
                ips.roi.commit(self.helper.pop(), self.oper)
        ips.update = True
    
    def mouse_move(self, ips, x, y, btn, **key):
        if ips.roi==None:return
        lim = 5.0/key['canvas'].get_scale()        
        if btn==None:
            self.cursor = wx.CURSOR_CROSS
            if ips.roi.snap(x, y, lim)!=None:
                self.cursor = wx.CURSOR_HAND
        elif btn==1:
            ips.roi.draged(self.odx, self.ody, x, y, self.curobj)
            ips.update = True
        self.odx, self.ody = x, y
        
    def on_switch(self):
        print 'hahaha'