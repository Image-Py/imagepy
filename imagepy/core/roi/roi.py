# -*- coding: utf-8 -*-
"""
Created on Wed Dec 21 15:05:16 2016
@author: yxl
"""
from .convert import roi2shape, shape2roi
from shapely.affinity import affine_transform
        
class ROI:
    def __init__(self):pass
        
    def buffer(self, r):
        return shape2roi(roi2shape(self).buffer(r, 4))
        
    def convex(self):
        return shape2roi(roi2shape(self).convex_hull)
        
    def bounds(self):
        from .rectangleroi import RectangleRoi
        box = roi2shape(self).bounds
        return RectangleRoi(*box)
        
    def clip(self, rect):
        return shape2roi(roi2shape(rect).intersection(roi2shape(self)))
        
    def invert(self, rect):
        return shape2roi(roi2shape(rect).difference(roi2shape(self)))

    def union(self, roi):
        return shape2roi(roi2shape(roi).union(roi2shape(self)))
        
    def diff(self, roi):
        return shape2roi(roi2shape(self).difference(roi2shape(roi)))

    def affine(self, m, o):
        mat = [m[0,0], m[0,1], m[1,0], m[1,1], o[0], o[1]]
        return shape2roi(affine_transform(roi2shape(self), mat))
