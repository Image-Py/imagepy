# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 22:21:32 2017

@author: yxl
"""

import wx
from core.engine import Tool
import numpy as np
from .setting import Setting

class Plugin(Tool):
    title = 'Measure Setting'
    para = Setting
    view = [('color', 'line', 'color', 'color'),
    		('color', 'text', 'tcolor', 'color')]

    def __init__(self):
        pass
            
    def mouse_down(self, ips, x, y, btn, **key):
    	pass