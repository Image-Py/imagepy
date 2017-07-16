# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 23:24:43 2016

@author: yxl
"""
import wx 
from imagepy.core.engine import Free, Macros
from imagepy.core.manager import TextLogManager
from imagepy.ui.macroseditor import MacrosEditor
from imagepy import IPy

class Recorder(Free):
    title = 'Macros Recorder'
    asyn = False
    
    def run(self, para = None):
        if TextLogManager.get('Recorder')==None:
            MacrosEditor('Recorder').Show()
            
class Edit(Free):
    title = 'Macros Editor'
    asyn = False
    
    def run(self, para = None):
        MacrosEditor(TextLogManager.name('Macros Editor')).Show()
        
class Run(Free):
    title = 'Run Macros'
    para = {'path':''}
    
    def show(self):
        filt = 'Macros files (*.mc)|*.mc'
        return IPy.getpath('open..', filt, 'open', self.para)
        
    def run(self, para = None):
        f = open(para['path'])
        lines = f.readlines()
        f.close()
        Macros('noname', lines).start()

## three MacroRecoder class 
plgs = [Recorder, Edit, Run]