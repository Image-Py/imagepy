# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 23:24:32 2017
@author: yxl
"""
#from __future__ import absolute_import
from ... import root_dir

import numpy as np
import os, wx
import sys
from glob import glob




# read from the lut binarycode
# glob: return a list ot paths matching a pathname pattern.
filenames = glob(os.path.join(root_dir,'data/luts/*.lut'))
keys = [os.path.split(filename)[-1][:-4] for filename in filenames]
values = [np.fromfile(filename, dtype=np.uint8).reshape((3,256)).T.copy() for filename in filenames]

class ColorManager:
    luts = dict(zip(keys, values))
    frontcolor = (255,255,0)
    backcolor = (0,0,0)
    wr, wg, wb = 1.0/3, 1.0/3, 1.0/3
    
    @classmethod
    def get_color(cls, app=None):
        rst = None
        dlg = wx.ColourDialog(app)
        dlg.GetColourData().SetChooseFull(True)
        if dlg.ShowModal() == wx.ID_OK:
            rst = dlg.GetColourData().GetColour()
        dlg.Destroy()
        return rst

    @classmethod
    def set_front(cls, color):
        if not hasattr(color, '__len__'):
            color = (color, color, color)
        cls.frontcolor=tuple(color)

    @classmethod
    def set_back(cls, color):
        if not hasattr(color, '__len__'):
            color = (color, color, color)
        cls.backcolor=tuple(color)

    @classmethod
    def get_front(cls, one=False):
        if not one:return cls.frontcolor
        return np.dot((cls.wr,cls.wg,cls.wb), cls.frontcolor)

    @classmethod
    def get_back(cls, one):
        if not one:return cls.backcolor
        return np.dot((cls.wr,cls.wg,cls.wb), cls.backcolor)

    @classmethod
    def get_lut(cls, name='grays'):
        if name=='grays':
            lut = np.arange(256).reshape((-1,1))
            return (lut*np.ones((1,3))).astype(np.uint8)
        else: return cls.luts[name].copy()