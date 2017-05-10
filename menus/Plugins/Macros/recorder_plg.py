# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 23:24:43 2016

@author: yxl
"""
import wx 
from core.engines import Free
from core.managers import TextLogManager
from ui.macroseditor import MacrosEditor
import IPy

class Recorder(Free):
    title = 'Macros Recorder'
    
    def run(self, para = None):
        if TextLogManager.get('Recorder')==None:
            f = lambda : MacrosEditor('Recorder').Show()
            wx.CallAfter(f)
            
class Edit(Free):
    title = 'Macros Editor'
    
    def run(self, para = None):
        f = lambda : MacrosEditor(TextLogManager.name('Macros Editor')).Show()
        wx.CallAfter(f)
        
class Run(Free):
    title = 'Run Macros'
    para = {'path':''}
    
    def show(self):
        filt = 'Macros files (*.mc)|*.mc'
        return IPy.getpath('open..', filt, self.para)
        
    def run(self, para = None):
        f = open(para['path'])
        lines = f.readlines()
        f.close()
        IPy.run_macros(lines)

## three MacroRecoder class 
plgs = [Recorder, Edit, Run]