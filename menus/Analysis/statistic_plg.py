# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 20:34:59 2016
@author: yxl
"""
import IPy
import numpy as np
from core.engines import Simple

class Histogram(Simple):
    title = 'Histogram'
    note = ['8-bit', '16-bit']
    
    para = {'fre':True, 'slice':False}
    view = [(bool, 'count frequence', 'fre'),
            (bool, 'each slices', 'slice')]
        
    def run(self, ips, imgs, para = None):
        if not para['slice']: imgs = [ips.get_img()]
        data = []
        for i in range(len(imgs)):
            maxv = imgs[i].max()
            if maxv==0:continue
            ct = np.histogram(imgs[i], maxv, [1,maxv+1])[0]
            titles = ['slice','value','count']
            dt = [[i]*len(ct), list(range(maxv+1)), ct]
            if not para['slice']:
                titles, dt = titles[1:], dt[1:]
            if self.para['fre']:
                fre = ct/float(ct.sum())
                titles.append('frequence')
                dt.append(fre.round(4))
            dt = list(zip(*dt))
            data.extend(dt)

        IPy.table(ips.title+'-histogram', data, titles)
        
class Statistic(Simple):
    title = 'Statistic'
    note = ['8-bit', '16-bit']
    
    para = {'max':True, 'min':True,'mean':False,'var':False,'std':False,'stack':False}
    view = [(bool, 'Max', 'max'),
            (bool, 'Min', 'min'),
            (bool, 'Mean', 'mean'),
            (bool, 'Variance', 'var'),
            (bool, 'Standard', 'std')]
    
    def load(self, ips):
        self.view = self.view[:5]
        if ips.get_nslices()>1:
            self.view.append((bool, 'count every stack', 'stack'))
        return True
        
    def count(self, img, para):
        rst = []
        if para['max']: rst.append(img.max())
        if para['min']: rst.append(img.min())
        if para['mean']: rst.append(img.mean().round(4))
        if para['var']: rst.append(img.var().round(4))
        if para['std']: rst.append(img.std().round(4))
        return rst
        
    def run(self, ips, imgs, para = None):
        titles = ['Max','Min','Mean','Variance','Standard']
        key = {'Max':'max','Min':'min','Mean':'mean','Variance':'var','Standard':'std'}
        titles = [i for i in titles if para[key[i]]]

        if self.para['stack']:
            data = []
            for n in range(ips.get_nslices()):
                data.append(self.count(imgs[n], para))
                IPy.set_progress(round((n+1)*100.0/len(imgs)))
            IPy.set_progress(0)
        else: data = [self.count(ips.get_img(), para)]
        IPy.table(ips.title+'-statistic', data, titles)
        
plgs = [Histogram, Statistic]