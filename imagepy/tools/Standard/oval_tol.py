# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 17:35:09 2016

@author: yxl
"""
from imagepy.core.roi import ovalroi
import numpy as np
import wx
from .polygon_tol import Polygonbuf
from imagepy.core.engine import Tool

class Plugin(Tool):
    title = 'Ellipse'
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
                    ips.roi.info(ips, self.curobj)
                if not self.curobj in (None,True):return
                self.oper = '+'
                if ips.roi==None or not hasattr(ips.roi, 'topolygon'):
                    ips.roi = ovalroi.OvalRoi()
                    self.doing = True
                    ips.roi.lt, ips.roi.tp = x, y
                    ips.roi.rt, ips.roi.bm = x, y
                    self.curobj = 'rb'
                    self.odx, self.ody = x,y
                elif hasattr(ips.roi, 'topolygon'):
                    self.odx, self.ody = x, y
                    self.ox, self.oy = x, y
                    if key['shift']: 
                        ips.roi = ips.roi.topolygon()
                        self.oper,self.doing,self.curobj = '+',True,None
                    elif key['ctrl']: 
                        ips.roi = ips.roi.topolygon()
                        self.oper,self.doing,self.curobj = '-',True,None
                    elif self.curobj: return
                    else: 
                        ips.roi = ovalroi.OvalRoi()
                        self.doing = True
                        ips.roi.lt, ips.roi.tp = x, y
                        ips.roi.rt, ips.roi.bm = x, y
                        self.curobj = 'rb'
                        self.odx, self.ody = x,y
                else: ips.roi = None

        ips.update = True

    def mouse_up(self, ips, x, y, btn, **key):
        if self.doing:
            self.doing = False
            self.curobj = None
            if ips.roi.dtype == 'rect':
                if not ips.roi.commit():ips.roi = None
            elif ips.roi.dtype == 'polygon':
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
            if ips.roi.dtype == 'polygon' and self.doing:
                l,b,r,t = self.ox, self.oy, x, y
                ar = np.linspace(0, np.pi*2,29)
                xs = np.cos(ar)*abs(r-l)/2+(r+l)/2
                ys = np.sin(ar)*abs(t-b)/2+(t+b)/2
                self.helper.buf = [[(x,y) for x,y in zip(xs,ys)],[]]
            if self.curobj: ips.roi.draged(self.odx, self.ody, x, y, self.curobj)
            ips.update = True
        self.odx, self.ody = x, y

    def mouse_wheel(self, ips, x, y, d, **key):
        pass