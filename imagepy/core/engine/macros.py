# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 01:48:23 2016
@author: yxl
"""
import wx
from ... import IPy
from ...core.manager import PluginsManager 
from wx.lib.pubsub import pub
from imagepy.core.manager import ReaderManager, ViewerManager
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
        if len(self.cmds[self.cur])<3 or self.cmds[self.cur][0] == '#':
            self.cur += 1
            return self._next(callafter)
        title, para = self.cmds[self.cur].split('>')
        self.cur += 1
        plg = PluginsManager.get(title)()
        plg.start(eval(para), self.next)

    def next(self):
        if IPy.uimode() == 'no':
            self._next(self)
        else: wx.CallAfter(pub.sendMessage, 'stepmacros', plg=self)

    def run(self):self.next()
        #IPy.run_macros(self.cmds)
        
    def __call__(self):
        return self
        
    def start(self, para=None, callafter=None):
        self.callafter = callafter
        self.cur = 0
        self.run()

def show_mc(data, title):
    wx.CallAfter(Macros(title, data).start)

ViewerManager.add('mc', show_mc)

def read_mc(path):
    f = open(path, encoding='utf-8')
    cont = f.readlines()
    f.close()
    print(cont)
    return cont

ReaderManager.add('mc', read_mc, tag='mc')