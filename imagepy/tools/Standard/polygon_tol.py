# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 17:35:09 2016

@author: yxl
"""
from imagepy.core.roi import polygonroi
import wx

class Polygonbuf:
    def __init__(self):
        self.buf = [[],[]]
        
    def addpoint(self, p):
        self.buf[0].append(p)
        
    def draw(self, dc, f, **key):
        dc.SetPen(wx.Pen((0,255,0), width=1, style=wx.SOLID))
        if len(self.buf[0])>1:
            dc.DrawLines([f(*i) for i in self.buf[0]])
        for i in self.buf[0]: dc.DrawCircle(f(*i),2)
    
    def pop(self):
        a = self.buf
        self.buf = [[],[]]
        return a
        
from imagepy.core.engine import Tool

class Plugin(Tool):
    title = 'Polygon'
    def __init__(self):
        self.curobj = None
        self.doing = False
        self.oper = ''
        self.helper = Polygonbuf()
            
    def mouse_down(self, ips, x, y, btn, **key): 
        lim = 5.0/key['canvas'].scale
        ips.mark = self.helper
        if btn==1:
            if not self.doing:
                if ips.roi!= None:
                    self.curobj = ips.roi.pick(x, y, ips.cur, lim)
                    ips.roi.info(ips, self.curobj)
                if not self.curobj in (None,True):return
                self.oper = '+'
                if ips.roi == None:
                    ips.roi = polygonroi.PolygonRoi()
                    self.doing = True
                elif hasattr(ips.roi, 'topolygon'):
                    if key['shift']: 
                        ips.roi = ips.roi.topolygon()
                        self.oper,self.doing = '+',True
                    elif key['ctrl']: 
                        ips.roi = ips.roi.topolygon()
                        self.oper,self.doing = '-',True
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
        ips.update()
    
    def mouse_move(self, ips, x, y, btn, **key):
        if ips.roi==None:return
        lim = 5.0/key['canvas'].scale      
        if btn==None:
            self.cursor = wx.CURSOR_CROSS
            if ips.roi.snap(x, y, ips.cur, lim)!=None:
                self.cursor = wx.CURSOR_HAND
        elif btn==1:
            ips.roi.draged(self.odx, self.ody, x, y, ips.cur, self.curobj)
            ips.update()
        self.odx, self.ody = x, y
        
    def on_switch(self):
        print('hahaha')