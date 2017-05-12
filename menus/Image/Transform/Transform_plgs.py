# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 01:14:50 2016
@author: yxl
"""
import numpy as np
import scipy.ndimage as nimg
from imagepy.core.engine import Filter

class Rotate(Filter):
    title = 'Rotate'
    note = ['all', 'auto_msk', 'auto_snap','preview']
    para = {'ang':0}
    view = [(float, (0,360), 1, 'angle', 'ang', 'degree')]
        
    def run(self, ips, snap, img, para = None):
        if para == None: para = self.para
        a = para['ang']/180.0*np.pi
        o = np.array(ips.size)*0.5
        if ips.roi!=None:
            box = ips.roi.get_box()
            o = np.array([box[1]+box[3],box[0]+box[2]])*0.5
        trans = np.array([[np.cos(a),-np.sin(a)],[np.sin(a),np.cos(a)]])
        offset = o-trans.dot(o)
        nimg.affine_transform(snap, trans, output=img, offset=offset)
        
class Scale(Filter):
    title = 'Scale'
    note = ['all', 'auto_msk', 'auto_snap','preview']
    para = {'zoom':1}
    view = [(float, (0.1,10), 1, 'fact', 'zoom', '')]

    def run(self, ips, snap, img, para = None):
        if para == None: para = self.para
        k = 1/para['zoom']
        o = np.array(ips.size)*0.5
        if ips.roi!=None:
            box = ips.roi.get_box()
            o = np.array([box[1]+box[3],box[0]+box[2]])*0.5
        trans = np.array([[k,0],[0,k]])
        offset = o-trans.dot(o)
        nimg.affine_transform(snap, trans, output=img, offset=offset)

plgs = [Rotate, Scale]