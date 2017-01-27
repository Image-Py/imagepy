# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 22:51:57 2016

@author: yxl
"""

# -*- coding: utf-8 -*
import scipy.ndimage as nimg
from core.engines import Filter

class Closing(Filter):
    title = 'Binary Closeing'
    note = ['all', 'auto_msk', 'auto_snap','preview']

    #process
    def run(self, ips, snap, img, para = None):
        nimg.binary_closing(snap, output=img)
        img *= 255
        
class Opening(Filter):
    title = 'Binary Opening'
    note = ['all', 'auto_msk', 'auto_snap','preview']

    #process
    def run(self, ips, snap, img, para = None):
        nimg.binary_opening(snap, output=img)
        img *= 255
        
class Dilation(Filter):
    title = 'Binary Dilation'
    note = ['all', 'auto_msk', 'auto_snap','preview']

    #process
    def run(self, ips, snap, img, para = None):
        nimg.binary_dilation(snap, output=img)
        img *= 255
        
class Erosion(Filter):
    title = 'Binary Erosion'
    note = ['all', 'auto_msk', 'auto_snap','preview']

    #process
    def run(self, ips, snap, img, para = None):
        nimg.binary_erosion(snap, output=img)
        img *= 255
        
class FillHoles(Filter):
    title = 'Fill Holes'
    note = ['all', 'auto_msk', 'auto_snap','preview']

    #process
    def run(self, ips, snap, img, para = None):
        nimg.binary_fill_holes(snap, output=img)
        img *= 255
        
class EDT(Filter):
    title = 'Distance Transform'
    note = ['all', 'auto_msk', 'auto_snap','preview']

    #process
    def run(self, ips, snap, img, para = None):
        return nimg.distance_transform_edt(snap)
        
plgs = [Dilation, Erosion, Closing, Opening, FillHoles, EDT]