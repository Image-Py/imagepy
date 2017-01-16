# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 03:55:51 2016

@author: yxl
"""
import IPy
from ui.panelconfig import ParaDialog
from core.managers import WindowsManager, ToolsManager

class Tool:
    title = 'Tool'
    view, para, cfgv, cfgp = None, None, None, None
    def config(self):
        if self.cfgv != None:
            rst = IPy.getpara(self.title, self.cfgv, self.cfgp)
            if rst!=None: 
                self.on_config(self.cfgp)
                
           
    def show(self, ips):
        self.ips = ips
        if self.view==None:return
        self.on_load(ips)        
        self.dialog = ParaDialog(WindowsManager.get(), self.title)
        self.dialog.init_view(self.view, self.para, True, modal=False)
        self.dialog.set_handle(lambda x, p=self:p.run(
            ips, ips.snap, ips.get_img(), self.para))
        self.dialog.on_ok = lambda : self.on_ok(ips)
        self.dialog.on_cancel = lambda : self.on_cancel(ips)
        self.dialog.Show()
        #self.ips.update = True
    
    def on_config(self):pass
    def on_load(self, ips):pass
    def on_ok(self, ips):pass
    def on_cancel(self, ips):pass
    def run(self, ips):pass
    def on_switch(self):pass

    
    def start(self):ToolsManager.set(self)
    def mouse_down(self, ips, x, y, btn, **key): pass
    def mouse_up(self, ips, x, y, btn, **key): pass
    def mouse_move(self, ips, x, y, btn, **key): pass
    def mouse_wheel(self, ips, x, y, d, **key): pass