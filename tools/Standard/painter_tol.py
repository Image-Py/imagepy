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
    view = [(int, (0,30), 0,  'width', 'width', 'pix')]
    para = {'width':1}
    
    def __init__(self):
        self.sta = 0
        self.paint = paint.Paint()
        self.cursor = wx.CURSOR_CROSS
        
    def mouse_down(self, ips, x, y, btn, **key):
        self.sta = 1
        self.paint.set_curpt(x,y)
        ips.snapshot()
    
    def mouse_up(self, ips, x, y, btn, **key):
        self.sta = 0
    
    def mouse_move(self, ips, x, y, btn, **key):
        if self.sta==0:return
        self.paint.lineto(ips.img,x,y, self.para['width'])
        ips.update = 'pix'
        
    def mouse_wheel(self, ips, x, y, d, **key):pass