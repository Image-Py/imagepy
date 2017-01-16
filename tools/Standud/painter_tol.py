# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 17:35:09 2016

@author: yxl
"""
from core.draw import paint
import wx
from core.engines import Tool

class Plugin(Tool):
    title = 'Pencil'
    cfgv = [(int, (0,30), 0,  u'width', 'width', 'pix')]
    cfgp = {'width':1}
    
    def __init__(self):
        self.sta = 0
        self.paint = paint.Paint()
        self.paint.color = 255
        self.cursor = wx.CURSOR_CROSS
        
    def mouse_down(self, ips, x, y, btn, **key):
        if btn==3:
            self.paint.color = ips.get_img()[y,x]
            return
        self.sta = 1
        self.paint.set_curpt(x,y)
        ips.snapshot()
    
    def mouse_up(self, ips, x, y, btn, **key):
        self.sta = 0
    
    def mouse_move(self, ips, x, y, btn, **key):
        if self.sta==1:
            #self.paint.draw_point(ips.getimg(), x, y)
            self.paint.lineto(ips.get_img(),x,y, self.cfgp['width'])
            ips.update = True
        
    def mouse_wheel(self, ips, x, y, d, **key):
        print x,y,d,key