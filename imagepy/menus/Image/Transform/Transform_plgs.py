# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 01:14:50 2016
@author: yxl
"""
import numpy as np
import scipy.ndimage as nimg
from sciapp.action import Filter, Simple
from imagepy.ipyalg import linear_polar, polar_linear

class Rotate(Filter):
    title = 'Rotate'
    note = ['all', 'auto_msk', 'auto_snap','preview']
    para = {'ang':0}
    view = [(float, 'ang', (0,360), 1, 'angle', 'degree')]
        
    def run(self, ips, snap, img, para = None):
        if para == None: para = self.para
        a = para['ang']/180.0*np.pi
        o = np.array(ips.shape)*0.5
        if ips.roi!=None:
            box = ips.roi.box
            o = np.array([box[1]+box[3],box[0]+box[2]])*0.5
        trans = np.array([[np.cos(a),-np.sin(a)],[np.sin(a),np.cos(a)]])
        offset = o-trans.dot(o)
        nimg.affine_transform(snap, trans, output=img, offset=offset)
        
class Scale(Filter):
    title = 'Scale'
    note = ['all', 'auto_msk', 'auto_snap','preview']
    para = {'zoom':1}
    view = [(float, 'zoom', (0.1,10), 1, 'fact', '')]

    def run(self, ips, snap, img, para = None):
        if para == None: para = self.para
        k = 1/para['zoom']
        o = np.array(ips.shape)*0.5
        if ips.roi!=None:
            box = ips.roi.box
            o = np.array([box[1]+box[3],box[0]+box[2]])*0.5
        trans = np.array([[k,0],[0,k]])
        offset = o-trans.dot(o)
        nimg.affine_transform(snap, trans, output=img, offset=offset)

class LinearPolar(Simple):
    title = 'Linear To Polar'
    note = ['all']
    para = {'ext':'crop', 'order':1, 'slices':False}
    view = [(list, 'ext', ['full', 'crop'], str, 'extent', ''),
            (int, 'order', (0, 5), 0, 'interpolate', 'order'),
            (bool, 'slices', 'slices')]

    def run(self, ips, imgs, para):
        if not para['slices']: imgs = [ips.img]
        r, rst = min(ips.shape[:2])/2 if para['ext']=='crop' else None, []
        for i in range(len(imgs)):
            self.progress(i, len(imgs))
            rst.append(linear_polar(imgs[i], None, r, para['order']))
        self.app.show_img(rst, ips.title + '-polar')

class PolarLinear(Simple):
    title = 'Polar To Linear'
    note = ['all']
    para = {'ext':'crop', 'order':1, 'slices':False}
    view = [(list, 'ext', ['full', 'crop'], str, 'extent', ''),
            (int, 'order', (0, 5), 0, 'interpolate', 'order'),
            (bool, 'slices', 'slices')]

    def run(self, ips, imgs, para):
        if not para['slices']: imgs = [ips.img]
        r, rst = round(ips.shape[0]/(2**0.5 if para['ext']=='crop' else 1)), []
        for i in range(len(imgs)):
            self.progress(i, len(imgs))
            rst.append(polar_linear(imgs[i], None, int(r), para['order']))
        self.app.show_img(rst, ips.title + '-polar')

plgs = [Rotate, Scale, LinearPolar, PolarLinear]