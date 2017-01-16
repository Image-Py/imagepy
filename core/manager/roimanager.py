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
        if not cls.rois.has_key(name):
            return None
        return cls.rois[name]
        