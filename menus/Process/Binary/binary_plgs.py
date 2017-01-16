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
    def run(self, ips, img, buf, para = None):
        nimg.binary_closing(img, output=buf)
        buf *= 255
        return buf
        
class Opening(Filter):
    title = 'Binary Opening'
    note = ['all', 'auto_msk', 'auto_snap','preview']

    #process
    def run(self, ips, img, buf, para = None):
        nimg.binary_opening(img, output=buf)
        buf *= 255
        return buf
        
class Dilation(Filter):
    title = 'Binary Dilation'
    note = ['all', 'auto_msk', 'auto_snap','preview']

    #process
    def run(self, ips, img, buf, para = None):
        nimg.binary_dilation(img, output=buf)
        buf *= 255
        return buf
        
class Erosion(Filter):
    title = 'Binary Erosion'
    note = ['all', 'auto_msk', 'auto_snap','preview']

    #process
    def run(self, ips, img, buf, para = None):
        nimg.binary_erosion(img, output=buf)
        buf *= 255
        return buf
        
class FillHoles(Filter):
    title = 'Fill Holes'
    note = ['all', 'auto_msk', 'auto_snap','preview']

    #process
    def run(self, ips, img, buf, para = None):
        nimg.binary_fill_holes(img, output=buf)
        buf *= 255
        return buf
        
class EDT(Filter):
    title = 'Distance Transform'
    note = ['all', 'auto_msk', 'auto_snap','preview']

    #process
    def run(self, ips, img, buf, para = None):
        return nimg.distance_transform_edt(img)
        
plgs = [Dilation, Erosion, Closing, Opening, FillHoles, EDT]