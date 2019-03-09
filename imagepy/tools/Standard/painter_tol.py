# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 17:35:09 2016

@author: yxl
"""
from imagepy.core.draw import paint
from imagepy.core.engine import Tool
import wx

class Plugin(Tool):
    title = 'Pencil'
    view = [(int, 'width', (0,30), 0,  'width', 'pix')]
    para = {'width':1}
    
    def __init__(self):
        self.sta = 0
        self.paint = paint.Paint()
        self.cursor = wx.CURSOR_CROSS
        
    def mouse_down(self, ips, x, y, btn, **key):
        self.sta = 1
        self.paint.set_curpt(int(x), int(y))
        ips.snapshot()
    
    def mouse_up(self, ips, x, y, btn, **key):
        self.paint.lineto(ips.img, int(x), int(y), self.para['width'])
        ips.update()
        self.sta = 0
    
    def mouse_move(self, ips, x, y, btn, **key):
        if self.sta==0:return
        self.paint.lineto(ips.img, int(x), int(y), self.para['width'])
        ips.update()
        
    def mouse_wheel(self, ips, x, y, d, **key):pass