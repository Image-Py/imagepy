# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 17:35:09 2016

@author: yxl
"""
from imagepy.core.roi import lineroi
import wx
from imagepy.core.engine import Tool

class Linebuf:
    """Linebuf class"""
    def __init__(self):
        self.buf = []
        
    def addpoint(self, p):
        self.buf.append(p)
        
    def draw(self, dc, f, **key):
        dc.SetPen(wx.Pen((0,255,255), width=1, style=wx.SOLID))
        if len(self.buf)>1:
            dc.DrawLines([f(*i) for i in self.buf])
        for i in self.buf:dc.DrawCircle(f(*i),2)
    
    def pop(self):
        a = self.buf
        self.buf = []
        return a

class Plugin(Tool):
    """FreeLinebuf class plugin with events callbacks"""
    title = 'Line'
    def __init__(self):
        self.curobj = None
        self.doing = False
        self.helper = Linebuf()
        self.odx,self.ody = 0, 0
            
    def mouse_down(self, ips, x, y, btn, **key):
        lim = 5.0/key['canvas'].get_scale()  
        ips.mark = self.helper
        if btn==1:
            if not self.doing:
                print(ips.roi)
                print(self.curobj)
                if ips.roi!= None:
                    self.curobj = ips.roi.pick(x, y, lim)
                    ips.roi.info(ips, self.curobj)
                if self.curobj!=None:return
                    
                if ips.roi == None:
                    print(1)
                    ips.roi = lineroi.LineRoi()
                    self.doing = True
                elif ips.roi.dtype=='line' and key['shift']:
                    print(2)
                    self.doing = True
                else: ips.roi = None
            if self.doing:
                self.helper.addpoint((x,y))
                self.curobj = (self.helper.buf, -1)
                self.odx, self.ody = x,y
            
        elif btn==3:
            if self.doing:
                self.helper.addpoint((x,y))
                self.doing = False
                ips.roi.addline(self.helper.pop())
        ips.update = True
    
    def mouse_up(self, ips, x, y, btn, **key):
        self.curobj = None
    
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
        
    def mouse_wheel(self, ips, x, y, d, **key):
        pass