# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 00:26:45 2016

@author: yxl
"""
import os, wx
from imagepy.core.engine import Free
from imagepy.core.engine import Simple
from imagepy.core.engine import Filter
from imagepy.tools.Measure.setting import Setting

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

class RealMarker(Filter):
    title = 'RealMarker'
    # note = ['all']
    note = ['all', 'auto_msk', 'auto_snap', 'preview', '2int']

    ## parameter

    para = {'num':0}
    view = [(float, 'num', (0,1000), 2, '0', '1000')]
    def run(self, ips, snap, img, para = None):
        ips.ratioRuler = para['num']
        print('current ratio is {}'.format(para['num']))
        Setting['ratioRuler'] = para['num']
        # img = snap

plgs = [NewFilter, NewSimple, NewFree, NewTool, RealMarker]