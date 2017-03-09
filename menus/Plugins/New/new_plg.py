# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 00:26:45 2016

@author: yxl
"""
from core.engines import Free
from wx.py.editor import EditorFrame

class NewFilter(Free):
    title = 'New Filter'

    def run(self, para = None):
        EditorFrame(filename='./menus/Plugins/New/demo_filter.py').Show()
        
class NewSimple(Free):
    title = 'New Simple'

    def run(self, para = None):
        EditorFrame(filename='./menus/Plugins/New/demo_simple.py').Show()
        
class NewFree(Free):
    title = 'New Free'

    def run(self, para = None):
        EditorFrame(filename='./menus/Plugins/New/demo_free.py').Show()
        
class NewTool(Free):
    title = 'New Tool'

    def run(self, para = None):
        EditorFrame(filename='./menus/Plugins/New/demo_tool.py').Show()
        
plgs = [NewFilter, NewSimple, NewFree, NewTool]