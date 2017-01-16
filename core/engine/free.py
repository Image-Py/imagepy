# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 03:57:53 2016

@author: yxl
"""
from ui.panelconfig import ParaDialog
from core.managers import TextLogManager
import IPy, wx

class Free:
    title = 'Free'
    view = None
    para = None
    
    def run(self, para=None):print 'this is a plugin'
        
    def load(self):return True
        
    def show(self):
        if self.view==None:return wx.ID_OK
        self.dialog = ParaDialog(IPy.get_window(), self.title)
        self.dialog.init_view(self.view, self.para, False, True)
        return self.dialog.ShowModal()
        
    def start(self, para=None):
        if not self.load():return
        if para!=None or self.show() == wx.ID_OK:
            if para==None:para = self.para
            win = TextLogManager.get('Recorder')
            if win!=None: win.append('%s>%s'%(self.title, para))
            self.run(para)