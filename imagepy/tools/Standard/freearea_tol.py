# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 17:35:09 2016

@author: yxl
"""
from imagepy.core.roi import polygonroi
import wx
from .polygon_tol import Polygonbuf
from imagepy.core.engine import Tool

class Plugin(Tool):
    """FreeArea class plugin with events callbacks"""
    title = 'Free Area'
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
                #self.oper = '+'
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
                self.odx, self.ody = x, y
        ips.update()
        
    def mouse_up(self, ips, x, y, btn, **key):
        if self.doing:
            self.helper.addpoint((x,y))
            self.doing = False
            self.curobj = None
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
            if self.doing:
                self.helper.addpoint((x,y))
            elif self.curobj: ips.roi.draged(self.odx, self.ody, x, y, ips.cur, self.curobj)
            ips.update()
        self.odx, self.ody = x, y
        
    def mouse_wheel(self, ips, x, y, d, **key):
        pass