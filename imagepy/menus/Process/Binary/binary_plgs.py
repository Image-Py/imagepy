# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 22:51:57 2016

@author: yxl
"""

# -*- coding: utf-8 -*
import scipy.ndimage as ndimg
import numpy as np
from sciapp.action import Filter
from skimage.morphology import convex_hull_object
from skimage.segmentation import clear_border

class Closing(Filter):
    """Closing: derived from sciapp.action.Filter """
    title = 'Binary Closing'
    note = ['8-bit', 'auto_msk', 'auto_snap','preview']
    para = {'w':3, 'h':3}
    view = [(int, 'w', (1,15), 0, 'width', 'pix'),
            (int, 'h', (1,15), 0, 'height', 'pix')]

    def run(self, ips, snap, img, para = None):
        strc = np.ones((para['h'], para['w']), dtype=np.uint8)
        ndimg.binary_closing(snap, strc, output=img)
        img *= 255
        
class Opening(Filter):
    """Opening: derived from sciapp.action.Filter """
    title = 'Binary Opening'
    note = ['8-bit', 'auto_msk', 'auto_snap','preview']
    para = {'w':3, 'h':3}
    view = [(int, 'w', (1,15), 0, 'width', 'pix'),
            (int, 'h', (1,15), 0, 'height', 'pix')]

    def run(self, ips, snap, img, para = None):
        strc = np.ones((para['h'], para['w']), dtype=np.uint8)
        ndimg.binary_opening(snap, strc, output=img)
        img *= 255
        
class Dilation(Filter):
    """Dilation: derived from sciapp.action.Filter """
    title = 'Binary Dilation'
    note = ['8-bit', 'auto_msk', 'auto_snap','preview']
    para = {'w':3, 'h':3}
    view = [(int, 'w', (1,15), 0, 'width', 'pix'),
            (int, 'h', (1,15), 0, 'height', 'pix')]

    def run(self, ips, snap, img, para = None):
        strc = np.ones((para['h'], para['w']), dtype=np.uint8)
        ndimg.binary_dilation(snap, strc, output=img)
        img *= 255
        
class Erosion(Filter):
    """Erosion: derived from sciapp.action.Filter """
    title = 'Binary Erosion'
    note = ['8-bit', 'auto_msk', 'auto_snap','preview']
    para = {'w':3, 'h':3}
    view = [(int, 'w', (1,15), 0, 'width', 'pix'),
            (int, 'h', (1,15), 0, 'height', 'pix')]

    def run(self, ips, snap, img, para = None):
        strc = np.ones((para['h'], para['w']), dtype=np.uint8)
        ndimg.binary_erosion(snap, strc, output=img)
        img *= 255
        
class Outline(Filter):
    """Outline: derived from sciapp.action.Filter """
    title = 'Binary Outline'
    note = ['8-bit', 'auto_msk', 'auto_snap','preview']

    def run(self, ips, snap, img, para = None):
        ndimg.binary_dilation(snap, output=img)
        img *= 255
        img -= snap
        
class FillHoles(Filter):
    """FillHoles: derived from sciapp.action.Filter """
    title = 'Fill Holes'
    note = ['8-bit', 'auto_msk', 'auto_snap','preview']

    def run(self, ips, snap, img, para = None):
        ndimg.binary_fill_holes(snap, output=img)
        img *= 255

class ClearBorder(Filter):
    title = 'Clear Border'
    note = ['8-bit', 'auto_msk', 'auto_snap']

    def run(self, ips, snap, img, para = None):
        clear_border(img, in_place=True)
        

class Convex(Filter):
    title = 'Binary ConvexHull'
    note = ['8-bit', 'auto_msk', 'auto_snap']

    def run(self, ips, snap, img, para = None):
        img[convex_hull_object(snap)] = 255
        

plgs = [Dilation, Erosion, '-', Closing, Opening, '-', Outline, FillHoles, ClearBorder, Convex]