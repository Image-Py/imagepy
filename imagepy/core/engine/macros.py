# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 01:48:23 2016
@author: yxl
"""
import wx
from ... import IPy
from ...core.manager import PluginsManager 
from wx.lib.pubsub import pub
from imagepy import IPy

def stepmacros(plg, callafter=None): 
    plg._next(callafter)
pub.subscribe(stepmacros, 'stepmacros')

class Macros:
    def __init__(self, title, cmds):
        self.title = title
        self.cmds = cmds
        
    def _next(self, callafter=None):
        if self.cur==len(self.cmds):
            if self.callafter!=None:
                self.callafter()
            return
        if self.cmds[self.cur][0] == '#':
            return self._next(callafter)
        title, para = self.cmds[self.cur].split('>')
        self.cur += 1
        plg = PluginsManager.get(title)()
        plg.start(eval(para), self.next)

    def next(self):
        wx.CallAfter(pub.sendMessage, 'stepmacros', plg=self)

    def run(self):self.next()
        #IPy.run_macros(self.cmds)
        
    def __call__(self):
        return self
        
    def start(self, para=None, callafter=None):
        self.callafter = callafter
        self.cur = 0
        self.run()