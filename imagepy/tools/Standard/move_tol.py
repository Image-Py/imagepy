# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 12:12:43 2016

@author: yxl
"""
import wx
from imagepy.core.engine import Tool

class Plugin(Tool):
    title = 'Move'
    def __init__(self):
        self.ox, self.oy = 0, 0
        self.cursor = wx.CURSOR_HAND
            
    def mouse_down(self, ips, x, y, btn, **key):
        self.ox, self.oy = key['canvas'].to_panel_coor(x,y)
    
    def mouse_up(self, ips, x, y, btn, **key):
        pass
    
    def mouse_move(self, ips, x, y, btn, **key):
        if btn==None:return
        x,y = key['canvas'].to_panel_coor(x,y)
        key['canvas'].move(x-self.ox, y-self.oy)
        self.ox, self.oy = x,y
        ips.update()
        
    def mouse_wheel(self, ips, x, y, d, **key):
        if d>0:key['canvas'].zoomout(x, y, 'data')
        if d<0:key['canvas'].zoomin(x, y, 'data')
        ips.update()