# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 01:48:23 2016

@author: yxl
"""
import IPy
from core.managers import TextLogManager

class Macros:
    def __init__(self, title, cmds):
        self.title = title
        self.cmds = cmds
        
    def run(self):
        IPy.run_macros(self.cmds)

    def __call__(self):
        return self
        
    def start(self, para=None):
        win = TextLogManager.get('Recorder')
        if win!=None: win.append('%s>None'%(self.title))
        self.run()
        