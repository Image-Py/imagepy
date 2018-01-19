# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 23:23:30 2017
@author: yxl
"""
import weakref

class ToolsManager:
    tools = {}
    curtool = None
    
    @classmethod
    def set(cls, tool):
        if tool.__class__ == cls.curtool.__class__:return
        if cls.curtool!=None: cls.curtool.switch()
        cls.curtool = tool
        
    @classmethod
    def add(cls, tol):cls.tools[tol.title] = tol
        
    @classmethod
    def get(cls, name=None):
        if name==None:return cls.curtool
        return cls.tools[name]
        
class PluginsManager:
    plgs = {}
    
    @classmethod
    def add(cls, plg):cls.plgs[plg.title] = plg
        
    @classmethod
    def get(cls, name):return cls.plgs[name]

class WidgetsManager:
    wgts, insts = {}, {}
    
    @classmethod
    def add(cls, wgt): cls.wgts[wgt.title] = wgt
        
    @classmethod
    def addref(cls, obj):
        cls.insts[obj.title] = weakref.ref(obj)

    @classmethod
    def get(cls, name):return cls.wgts[name]

    @classmethod
    def getref(cls, name):
        if not name in cls.insts: return None
        if cls.insts[name] is None: return None
        return cls.insts[name]()