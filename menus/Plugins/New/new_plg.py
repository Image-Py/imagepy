# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 00:26:45 2016

@author: yxl
"""
import os 
from core.engines import Free
from wx.py.editor import EditorFrame
import IPyGL

class NewFilter(Free):
    title = 'New Filter'

    def run(self, para = None):
        filename = os.path.join(IPyGL.root_dir,'./menus/Plugins/New/demo_filter.py')
        EditorFrame(filename=filename).Show()
        
class NewSimple(Free):
    title = 'New Simple'

    def run(self, para = None):
        filename = os.path.join(IPyGL.root_dir,'./menus/Plugins/New/demo_simple.py')
        EditorFrame(filename=filename).Show()
        
class NewFree(Free):
    title = 'New Free'

    def run(self, para = None):
        filename = os.path.join(IPyGL.root_dir,'./menus/Plugins/New/demo_free.py')
        EditorFrame(filename=filename).Show()
        
class NewTool(Free):
    title = 'New Tool'

    def run(self, para = None):
        filename = os.path.join(IPyGL.root_dir,'./menus/Plugins/New/demo_tool.py')
        EditorFrame(filename=filename).Show()
        
plgs = [NewFilter, NewSimple, NewFree, NewTool]