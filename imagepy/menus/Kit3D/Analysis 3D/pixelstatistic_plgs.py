import numpy as np
from sciapp.action import Simple, Filter
import pandas as pd

class Statistic(Simple):
    title = 'Pixel Statistic 3D'
    note = ['8-bit', '16-bit', 'int', 'float', 'stack3d']
    
    para = {'nozero':False, 'max':True, 'min':True,'mean':False,'var':False,'std':False,'slice':False}
    view = [(bool, 'nozero', 'no-zero'),
            ('lab', None, '=========  indecate  ========='),
            (bool, 'max', 'max'),
            (bool, 'min', 'min'),
            (bool, 'mean', 'mean'),
            (bool, 'variance', 'var'),
            (bool, 'standard', 'std'),
            (bool, 'slice', 'slice')]
        
    def count(self, img, para):
        rst = []
        if para['max']: rst.append(img.max())
        if para['min']: rst.append(img.min())
        if para['mean']: rst.append(img.mean().round(2))
        if para['var']: rst.append(img.var().round(2))
        if para['std']: rst.append(img.std().round(2))
        return [rst]
        
    def run(self, ips, imgs, para = None):
        titles = ['Max','Min','Mean','Variance','Standard']
        key = {'Max':'max','Min':'min','Mean':'mean','Variance':'var','Standard':'std'}
        titles = [i for i in titles if para[key[i]]]
        if para['nozero']: imgs = imgs[imgs!=0]
        data = self.count(imgs, para)
        self.app.show_table(pd.DataFrame(data, columns=titles), ips.title+'-statistic')

class Frequence(Simple):
    title = 'Frequence 3D'
    note = ['8-bit', '16-bit', 'int', 'float', 'stack3d']
    
    para = {'nozero':False, 'bins':0}
    view = [(int, 'bins', (0,1e4), 0, 'bins', 'count'),
            (bool, 'nozero', 'no-zero')]
        
    def run(self, ips, imgs, para = None):
        if para['nozero']: imgs = imgs[imgs!=0]
        minv, maxv = imgs.min(), imgs.max()
        bins = para['bins']
        if bins==0:bins = int(maxv - minv)+1
        ct, bins = np.histogram(imgs, bins, [minv, maxv+1])
        titles = ['value','count','frequence']
        dt = [bins[:-1].round(2), ct, (ct/ct.sum()).round(4)]
        dt = list(zip(*dt))

        self.app.show_table(pd.DataFrame(dt, columns=titles), ips.title+'-histogram')

plgs = [Statistic, Frequence]