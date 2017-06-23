# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 01:48:23 2016
@author: yxl
"""
from ... import IPy
from ...core.manager import TextLogManager, PluginsManager 
import threading

class Macros:
    def __init__(self, title, cmds):
        self.title = title
        self.cmds = cmds
        self.cur = 0
        
    def next(self):
        if self.cur==len(self.cmds): return
        if self.cmds[self.cur][0] == '#':
            return self.next()
        title, para = self.cmds[self.cur].split('>')
        self.cur += 1
        plg = PluginsManager.get(title)()
        print(type(plg))
        callback = lambda p=self:IPy.step_macros(p)
        plg.start(eval(para), callback)

    def run(self):
        self.next()
        #IPy.run_macros(self.cmds)
        

    def __call__(self):
        return self
        
    def start(self, thd=False):
        win = TextLogManager.get('Recorder')
        if win!=None and self.title!=None:
            win.append('{}>None'.format(self.title))
        self.run()