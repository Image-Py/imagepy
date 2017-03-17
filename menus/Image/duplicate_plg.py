# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 19:47:34 2016

@author: yxl
"""

from core.engines import Simple
from imageplus import ImagePlus
from ui.canvasframe import CanvasFrame
import numpy as np
import IPy

class Plugin(Simple):
    title = 'Duplicate'
    note = ['all']
    
    para = {'name':'Undefined','stack':True}
    
    def load(self, ips):
        self.para['name'] = ips.title+'-copy'
        self.view = [(str, 'Name', 'name','')]
        if ips.get_nslices()>1:
            self.view.append((bool, 'duplicate stack', 'stack'))
        return True
    #process
    def run(self, ips, imgs, para = None):
        name = self.para['name']
        if ips.get_nslices()==1 or self.para['stack']==False:
            if ips.roi == None:
                img = ips.get_img().copy()
                ipsd = ImagePlus([img], name)
            else:
                img = ips.get_subimg().copy()
                ipsd = ImagePlus([img], name)
                box = ips.roi.get_box()
                ipsd.roi = ips.roi.affine(np.eye(2), (-box[0], -box[1]))
        elif ips.get_nslices()>1 and self.para['stack']:
            if ips.roi == None:
                if ips.is3d:imgs=imgs.copy()
                else:imgs = [i.copy() for i in imgs]
            else:
                sc, sr = ips.get_rect()
                if ips.is3d: imgs=imgs[:, sc, sr].copy()
                else: imgs = [i[sc,sr].copy() for i in imgs]
            ipsd = ImagePlus(imgs, name)
            if ips.roi != None:
                ipsd.roi = ips.roi.affine(np.eye(2), (-sr.start, -sc.start))
        
        IPy.show_ips(ipsd)