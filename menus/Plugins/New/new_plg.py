# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 00:26:45 2016

@author: yxl
"""
import os, wx
from imagepy.core.engine import Free
from wx.py.editor import EditorFrame
from wx.lib.pubsub import pub
from imagepy import root_dir

def showeditor(filename=None): EditorFrame(filename=filename).Show()
pub.subscribe(showeditor, 'showeditor')

class NewFilter(Free):
    title = 'New Filter'

    def run(self, para = None):
        filename = os.path.join(root_dir,'./menus/Plugins/New/demo_filter.py')
        wx.CallAfter(pub.sendMessage, 'showeditor', filename=filename)
        
class NewSimple(Free):
    title = 'New Simple'

    def run(self, para = None):
        filename = os.path.join(root_dir,'./menus/Plugins/New/demo_simple.py')
        wx.CallAfter(pub.sendMessage, 'showeditor', filename=filename)
        
class NewFree(Free):
    title = 'New Free'

    def run(self, para = None):
        filename = os.path.join(root_dir,'./menus/Plugins/New/demo_free.py')
        wx.CallAfter(pub.sendMessage, 'showeditor', filename=filename)
        
class NewTool(Free):
    title = 'New Tool'

    def run(self, para = None):
        filename = os.path.join(root_dir,'./menus/Plugins/New/demo_tool.py')
        wx.CallAfter(pub.sendMessage, 'showeditor', filename=filename)
        
plgs = [NewFilter, NewSimple, NewFree, NewTool]