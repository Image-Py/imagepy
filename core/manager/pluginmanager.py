# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 23:23:30 2017

@author: yxl
"""
class ToolsManager:
    tools = {}
    curtool = None
    
    @classmethod
    def set(cls, tool):
        if tool.__class__ == cls.curtool.__class__:return
        if cls.curtool!=None: cls.curtool.on_switch()
        cls.curtool = tool
        
    @classmethod
    def add(cls, tol):cls.tools[tol.title] = tol
        
    @classmethod
    def get(cls, name):return cls.tools[name]
        
class PluginsManager:
    plgs = {}
    
    @classmethod
    def add(cls, plg):cls.plgs[plg.title] = plg
        
    @classmethod
    def get(cls, name):return cls.plgs[name]