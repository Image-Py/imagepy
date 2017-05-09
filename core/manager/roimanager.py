# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 23:26:14 2017

@author: yxl
"""

class RoiManager:
    rois = {}
    @classmethod
    def add(cls, name, roi):
        cls.rois[name] = roi
        
    @classmethod
    def get(cls, name):
        if name not in cls.rois:
            return None
        return cls.rois[name]
        