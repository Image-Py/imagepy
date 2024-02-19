# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 22:56:50 2016
@author: yxl
"""
import numpy as np
from sciapp.action import Filter
import scipy.ndimage as ndimg
from skimage.filters import\
    threshold_otsu, threshold_yen,\
    threshold_isodata, threshold_li, threshold_local,\
    threshold_minimum, threshold_mean, threshold_niblack,\
    threshold_sauvola, threshold_triangle, apply_hysteresis_threshold
from ...Image.Adjust.threshold_plg import Plugin as ThresholdPlg

class SimpleThreshold(ThresholdPlg):
    title = 'Simple Threshold'

class Hysteresis(Filter):
    title = 'Hysteresis Threshold'
    note = ['all', 'auto_msk', 'auto_snap', 'preview']
    modal = False

    def load(self, ips):
        minv, maxv = ips.range
        self.para = {'low':maxv, 'high':maxv}
        self.view = [('slide', 'low', (minv, maxv), 4, 'Low'),
                     ('slide', 'high', (minv, maxv), 4, 'High')]

        self.buflut = ips.lut
        ips.lut = ips.lut.copy()
        return True

    def cancel(self, ips):
        ips.lut = self.buflut
        ips.update()

    def preview(self, ips, para):
        ips.lut[:] = self.buflut
        minv, maxv = ips.range
        lim1 = (para['low']-minv)*255/(maxv-minv)
        lim2 = (para['high']-minv)*255/(maxv-minv)
        ips.lut[int(lim1):] = [0,255,0]
        ips.lut[int(lim2):] = [255,0,0]
        ips.update()

    def run(self, ips, snap, img, para = None):
        ips.lut = self.buflut
        return apply_hysteresis_threshold(snap, para['low'], para['high'])*ips.range[1]

class Auto(Filter):
    title = 'Auto Threshold'
    note = ['all', 'auto_msk', 'auto_snap', 'preview']
    para = {'method':'Otsu'}
    view = [(list, 'method', ['Otsu', 'Yen', 'Isodata', 'Li', 
        'Mini', 'Mean', 'Triangle'], str, 'Method', '')]

    def run(self, ips, snap, img, para = None):
        key = {'Otsu':threshold_otsu, 'Yen':threshold_yen, 
            'Isodata':threshold_isodata, 'Li':threshold_li,
            'Mini':threshold_minimum, 'Mean':threshold_mean,
            'Triangle':threshold_triangle}
        img[:] = (snap>key[para['method']](snap))*ips.range[1]

class Local(Filter):
    title = 'Adaptive Threshold'
    note = ['all', 'auto_msk', 'auto_snap', 'preview']
    para = {'method':'Mean', 'size':9, 'offset':2}
    view = [(list, 'method', ['Gaussian', 'Mean', 'Median'], str, 'method', ''),
            (int, 'size', (3, 31), 0, 'blocksize', 'pix'),
            (int, 'offset', (0, 50), 0, 'offset', '')]
    
    def run(self, ips, snap, img, para = None):
        img[:] = (snap>threshold_local(snap, para['size'], para['method'].lower(), para['offset']))*ips.range[1]

class Niblack(Filter):
    title = 'Niblack Threshold'
    note = ['all', 'auto_msk', 'auto_snap', 'preview']
    para = {'size':15, 'k':0.2}
    view = [(int, 'size', (3, 30), 0, 'blocksize', 'pix'),
            (float, 'k', (0, 1), 2, 'offset', '')]
    
    def run(self, ips, snap, img, para = None):
        if para['size']%2==0: return self.app.alert('size must be Odd')
        img[:] = (snap>threshold_niblack(snap, para['size'], para['k']))*ips.range[1]

class Sauvola(Filter):
    title = 'Sauvola Threshold'
    note = ['all', 'auto_msk', 'auto_snap', 'preview']
    para = {'size':15, 'k':0.2}
    view = [(int, 'size', (3, 30), 0, 'blocksize', 'pix'),
            (float, 'k', (0, 1), 2, 'offset', '')]
    
    def run(self, ips, snap, img, para = None):
        if para['size']%2==0: return self.app.alert('size must be Odd')
        img[:] = (snap>threshold_sauvola(snap, para['size'], para['k']))*ips.range[1]

plgs = [SimpleThreshold, Auto, '-', Local, Niblack, Sauvola, '-', Hysteresis]