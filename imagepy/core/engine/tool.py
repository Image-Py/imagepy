# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 03:55:51 2016
@author: yxl
"""
from ... import IPy
from ...core.manager import ToolsManager

class Tool:
    title = 'Tool'
    view, para = None, None 
           
    def show(self):
        if self.view == None:return
        rst = IPy.get_para(self.title, self.view, self.para)
        if rst!=None : self.config()
    
    def config(self):pass
    def load(self):pass
    def switch(self):pass
    
    def start(self):
        ips = IPy.get_ips()
        if not ips is None and not ips.tool is None:
            ips.tool = None
            ips.update = True
        ToolsManager.set(self)
        
    def mouse_down(self, ips, x, y, btn, **key): pass
    def mouse_up(self, ips, x, y, btn, **key): pass
    def mouse_move(self, ips, x, y, btn, **key): pass
    def mouse_wheel(self, ips, x, y, d, **key): pass