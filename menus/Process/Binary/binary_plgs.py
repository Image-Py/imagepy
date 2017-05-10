# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 22:51:57 2016

@author: yxl
"""

# -*- coding: utf-8 -*
import scipy.ndimage as ndimg
from core.engines import Filter

class Closing(Filter):
    """Closing: derived from core.engines.Filter """
    title = 'Binary Closeing'
    note = ['8-bit', 'auto_msk', 'auto_snap','preview']

    def run(self, ips, snap, img, para = None):
        ndimg.binary_closing(snap, output=img)
        img *= 255
        
class Opening(Filter):
    """Opening: derived from core.engines.Filter """
    title = 'Binary Opening'
    note = ['8-bit', 'auto_msk', 'auto_snap','preview']

    def run(self, ips, snap, img, para = None):
        ndimg.binary_opening(snap, output=img)
        img *= 255
        
class Dilation(Filter):
    """Dilation: derived from core.engines.Filter """
    title = 'Binary Dilation'
    note = ['8-bit', 'auto_msk', 'auto_snap','preview']

    def run(self, ips, snap, img, para = None):
        ndimg.binary_dilation(snap, output=img)
        img *= 255
        
class Erosion(Filter):
    """Erosion: derived from core.engines.Filter """
    title = 'Binary Erosion'
    note = ['8-bit', 'auto_msk', 'auto_snap','preview']

    def run(self, ips, snap, img, para = None):
        ndimg.binary_erosion(snap, output=img)
        img *= 255
        
class Outline(Filter):
    """Outline: derived from core.engines.Filter """
    title = 'Binary Outline'
    note = ['8-bit', 'auto_msk', 'auto_snap','preview']

    def run(self, ips, snap, img, para = None):
        ndimg.binary_dilation(snap, output=img)
        img *= 255
        img -= snap
        
class FillHoles(Filter):
    """FillHoles: derived from core.engines.Filter """
    title = 'Fill Holes'
    note = ['8-bit', 'auto_msk', 'auto_snap','preview']

    def run(self, ips, snap, img, para = None):
        ndimg.binary_fill_holes(snap, output=img)
        img *= 255
        
class EDT(Filter):
    """EDT: derived from core.engines.Filter """
    title = 'Distance Transform'
    note = ['all', 'auto_msk', 'auto_snap','preview']

    def run(self, ips, snap, img, para = None):
        return ndimg.distance_transform_edt(snap)
        
plgs = [Dilation, Erosion, '-', Closing, Opening, '-', Outline, FillHoles, EDT]