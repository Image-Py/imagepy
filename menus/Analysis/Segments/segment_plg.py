# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 01:06:59 2016

@author: yxl
"""
import IPy
import numpy as np
from core.engines import Simple
from scipy import ndimage
from core.managers import WindowsManager
from core.roi.pointroi import PointRoi

class Statistic(Simple):
    title = 'Segments Statistic'
    note = ['8-bit', '16-bit']
    
    para = {'lab':None, 'max':True, 'min':True,'mean':False,'var':False,'std':False,'sum':False}
    view = [('img', 'Label', 'lab', ''),
            (bool, 'Max', 'max'),
            (bool, 'Min', 'min'),
            (bool, 'Mean', 'mean'),
            (bool, 'Standard', 'std'),
            (bool, 'Sum', 'sum')]
            
    #process
    def run(self, ips, imgs, para = None):
        lab = WindowsManager.get(para['lab']).ips.get_img()
        if lab.dtype != np.uint8 and lab.dtype != np.uint16:
            IPy.alert('Label image must be in type 8-bit or 16-bit')
            return
        index = range(1, lab.max()+1)
        titles = ['Max','Min','Mean','Variance','Standard','Sum']
        key = {'Max':'max','Min':'min','Mean':'mean','Variance':'var','Standard':'std','Sum':'sum'}
        titles = ['value'] + [i for i in titles if para[key[i]]]
        
        data = [index]
        img = ips.get_img()
        if img is lab: img = img>0
        if para['max']:data.append(ndimage.maximum(img, lab, index))
        if para['min']:data.append(ndimage.minimum(img, lab, index))        
        if para['mean']:data.append(ndimage.mean(img, lab, index).round(4))
        if para['var']:data.append(ndimage.variance(img, lab, index).round(4)) 
        if para['std']:data.append(ndimage.standard_deviation(img, lab, index).round(4))         
        if para['sum']:data.append(ndimage.sum(img, lab, index).round(4))         
        data = zip(*data)
        IPy.table(ips.title+'-segment', data, titles)
        
class Position(Simple):
    title = 'Segments Position'
    note = ['8-bit', '16-bit']
    
    para = {'lab':None, 'center':True,'max':False, 'min':False}
    view = [('img', 'Label', 'lab', ''),
            (bool, 'Center', 'center'),
            (bool, 'Max', 'max'),
            (bool, 'Min', 'min')]

    #process
    def run(self, ips, imgs, para = None):
        lab = WindowsManager.get(para['lab']).ips.get_img()
        if lab.dtype != np.uint8 and lab.dtype != np.uint16:
            IPy.alert('Label image must be in type 8-bit or 16-bit')
            return
        index = range(1, lab.max()+1)
        titles = ['Center-X','Center-Y', 'Max-X','Max-Y','Min-X','Min-Y']
        key = {'Max-X':'max','Max-Y':'max','Min-X':'min','Min-Y':'min','Center-X':'center','Center-Y':'center'}
        titles = ['value'] + [i for i in titles if para[key[i]]]
        
        data = [index]
        img = ips.get_img()
        if img is lab: img = img>0
        if para['center']:
            pos = np.round(ndimage.center_of_mass(img, lab, index), 2)
            data.append(pos[:,0])
            data.append(pos[:,1])  
        if para['max']:
            pos = np.round(ndimage.minimum_position(img, lab, index), 2)
            data.append(pos[:,0])
            data.append(pos[:,1])
        if para['min']:
            pos = np.round(ndimage.maximum_position(img, lab, index), 2)
            data.append(pos[:,0])
            data.append(pos[:,1])       
        data = zip(*data)
        IPy.table(ips.title+'-position', data, titles)
        
class Mark(Simple):
    title = 'Mark Points'
    note = ['8-bit', '16-bit']
    
    para = {'lab':None, 'mode':'Max'}
    view = [('img', 'Label', 'lab', ''),
            (list, ('Max','Min','Center'), str, 'Point', 'mode', 'pts')]

    #process
    def run(self, ips, imgs, para = None):
        lab = WindowsManager.get(para['lab']).ips.get_img()
        if lab.dtype != np.uint8 and lab.dtype != np.uint16:
            IPy.alert('Label image must be in type 8-bit or 16-bit')
            return
        index = range(1, lab.max()+1)
        data = [index]
        img = ips.get_img()
        if img is lab: img = img>0
        if para['mode'] == 'Center':
            pos = np.round(ndimage.center_of_mass(img, lab, index), 2)[:,::-1]
            data.append(pos[:,0])
            data.append(pos[:,1])  
        if para['mode'] == 'Max':
            pos = np.round(ndimage.maximum_position(img, lab, index), 2)[:,::-1]
            data.append(pos[:,0])
            data.append(pos[:,1])
        if para['mode'] == 'Min':
            pos = np.round(ndimage.minimum_position(img, lab, index), 2)[:,::-1]
            data.append(pos[:,0])
            data.append(pos[:,1])       
        body = [tuple(i) for i in pos]
        ips.roi = PointRoi(body)
        
plgs = [Statistic, Position, Mark]