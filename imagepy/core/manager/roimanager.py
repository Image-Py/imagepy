# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 23:26:14 2017
@author: yxl
"""
from .configmanager import ConfigManager

class RoiManager:
    rois = {}
    @classmethod
    def add(cls, name, roi):
        cls.rois[name] = roi
        
    @classmethod
    def remove(cls, name):
        if name in cls.rois: del cls.rois[name]

    @classmethod
    def get(cls, name):
        if name not in cls.rois:
            return None
        return cls.rois[name]
        
    @classmethod
    def get_titles(cls):
        return sorted(list(cls.rois.keys()))

    @classmethod
    def get_color(cls):
        color = ConfigManager.get('roicolor')
        if color is None:color = (255,255,0)
        return color

    @classmethod
    def set_color(cls, color):
        ConfigManager.set('roicolor', color)

    @classmethod
    def get_lw(cls):
        lw = ConfigManager.get('roilw')
        if lw is None:lw = 1
        return lw

    @classmethod
    def set_lw(cls, lw):
        ConfigManager.set('roilw', lw)