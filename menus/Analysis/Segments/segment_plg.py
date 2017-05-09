# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 01:06:59 2016

@author: yxl
"""
import IPy
import numpy as np
from core.engine import Simple
from scipy import ndimage
from core.manager import WindowsManager
from core.roi.pointroi import PointRoi

class Plugin(Simple):
    title = 'Segments Statistic'
    note = ['8-bit', '16-bit']
    
    para = {'lab':None, 'max':True, 'min':True,'mean':False,'var':False,'std':False,'sum':False}
    view = [('img', 'Label', 'lab', ''),
            (bool, 'max', 'max'),
            (bool, 'min', 'min'),
            (bool, 'mean', 'mean'),
            (bool, 'standard', 'std'),
            (bool, 'sum', 'sum')]
            
    #process
    def run(self, ips, imgs, para = None):
        lab = WindowsManager.get(para['lab']).ips.get_img()
        if lab.dtype != np.uint8 and lab.dtype != np.uint16:
            IPy.alert('Label image must be in type 8-bit or 16-bit')
            return
        index = list(range(1, lab.max()+1))
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
        data = list(zip(*data))
        IPy.table(ips.title+'-segment', data, titles)
        