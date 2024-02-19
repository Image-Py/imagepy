# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 00:26:45 2016

@author: yxl
"""
import os, wx
from sciapp.action import Free
from wx.py.editor import EditorFrame
from imagepy import root_dir

class NewFilter(Free):
    title = 'New Filter'
    asyn = False

    def run(self, para = None):
        filename = os.path.join(root_dir,'./menus/Plugins/New/demo_filter.py')
        EditorFrame(filename=filename).Show()
        
class NewSimple(Free):
    title = 'New Simple'
    asyn = False

    def run(self, para = None):
        filename = os.path.join(root_dir,'./menus/Plugins/New/demo_simple.py')
        EditorFrame(filename=filename).Show()
        
class NewFree(Free):
    title = 'New Free'
    asyn = False

    def run(self, para = None):
        filename = os.path.join(root_dir,'./menus/Plugins/New/demo_free.py')
        EditorFrame(filename=filename).Show()
        
class NewTool(Free):
    title = 'New Tool'
    asyn = False

    def run(self, para = None):
        filename = os.path.join(root_dir,'./menus/Plugins/New/demo_tool.py')
        EditorFrame(filename=filename).Show()
        
plgs = [NewFilter, NewSimple, NewFree, NewTool]