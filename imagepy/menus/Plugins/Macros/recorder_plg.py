# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 23:24:43 2016

@author: yxl
"""
import wx 
from imagepy.core.engine import Free, Macros
from imagepy import IPy

class Plugin(Free):
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