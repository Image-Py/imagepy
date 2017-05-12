# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 22:51:57 2016

@author: yxl
"""

# -*- coding: utf-8 -*
import scipy.ndimage as ndimg
from imagepy.core.engine import Filter

class Closing(Filter):
    """Closing: derived from imagepy.core.engine.Filter """
    title = 'Binary Closeing'
    note = ['8-bit', 'auto_msk', 'auto_snap','preview']

    def run(self, ips, snap, img, para = None):
        ndimg.binary_closing(snap, output=img)
        img *= 255
        
class Opening(Filter):
    """Opening: derived from imagepy.core.engine.Filter """
    title = 'Binary Opening'
    note = ['8-bit', 'auto_msk', 'auto_snap','preview']

    def run(self, ips, snap, img, para = None):
        ndimg.binary_opening(snap, output=img)
        img *= 255
        
class Dilation(Filter):
    """Dilation: derived from imagepy.core.engine.Filter """
    title = 'Binary Dilation'
    note = ['8-bit', 'auto_msk', 'auto_snap','preview']

    def run(self, ips, snap, img, para = None):
        ndimg.binary_dilation(snap, output=img)
        img *= 255
        
class Erosion(Filter):
    """Erosion: derived from imagepy.core.engine.Filter """
    title = 'Binary Erosion'
    note = ['8-bit', 'auto_msk', 'auto_snap','preview']

    def run(self, ips, snap, img, para = None):
        ndimg.binary_erosion(snap, output=img)
        img *= 255
        
class Outline(Filter):
    """Outline: derived from imagepy.core.engine.Filter """
    title = 'Binary Outline'
    note = ['8-bit', 'auto_msk', 'auto_snap','preview']

    def run(self, ips, snap, img, para = None):
        ndimg.binary_dilation(snap, output=img)
        img *= 255
        img -= snap
        
class FillHoles(Filter):
    """FillHoles: derived from imagepy.core.engine.Filter """
    title = 'Fill Holes'
    note = ['8-bit', 'auto_msk', 'auto_snap','preview']

    def run(self, ips, snap, img, para = None):
        ndimg.binary_fill_holes(snap, output=img)
        img *= 255
        
class EDT(Filter):
    """EDT: derived from imagepy.core.engine.Filter """
    title = 'Distance Transform'
    note = ['all', 'auto_msk', 'auto_snap','preview']

    def run(self, ips, snap, img, para = None):
        return ndimg.distance_transform_edt(snap)
        
plgs = [Dilation, Erosion, '-', Closing, Opening, '-', Outline, FillHoles, EDT]