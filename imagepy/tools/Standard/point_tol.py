# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 17:35:09 2016

@author: yxl
"""
from imagepy.core.roi import pointroi
import wx
from imagepy.core.engine import Tool

class Plugin(Tool):
    title = 'Point'
    def __init__(self):
        self.curobj, self.onobj = None, None
        self.odx, self.ody = 0, 0
            
    def mouse_down(self, ips, x, y, btn, **key):
        lim = 5.0/key['canvas'].get_scale()
        if btn==1:
            if ips.roi!=None:
                self.curobj = ips.roi.pick(x, y, ips.cur, lim)
                ips.roi.info(ips, self.curobj)
            if self.curobj!=None:return
            if not isinstance(ips.roi, pointroi.PointRoi):
                ips.roi = pointroi.PointRoi()
            if not key['shift']:del ips.roi.body[:]
            ips.roi.add((x,y,ips.cur))
            self.curobj = ips.roi.pick(x, y, ips.cur, lim)
            ips.update()
            self.odx, self.ody = x, y
    
    def mouse_up(self, ips, x, y, btn, **key):
        self.curobj = None
    
    def mouse_move(self, ips, x, y, btn, **key):
        if ips.roi==None:return
        lim = 5.0/key['canvas'].get_scale()
        if btn==None:
            self.cursor = wx.CURSOR_CROSS
            self.onobj = ips.roi.snap(x, y, ips.cur, lim)
            if self.onobj!=None:
                self.cursor = wx.CURSOR_HAND
        elif btn==1:
            ips.roi.draged(self.odx, self.ody, x, y, ips.cur, self.curobj)
            ips.update()
        self.odx, self.ody = x, y
        
    def mouse_wheel(self, ips, x, y, d, **key):
        lim = 5.0/key['canvas'].get_scale()
        if not isinstance(ips.roi, pointroi.PointRoi):return
        if not self.onobj is None:
            cur = ips.roi.body[self.onobj][2]
            ips.roi.draged(self.odx, self.ody, x, y, cur+d, self.onobj)
            ips.update()