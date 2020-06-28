# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 01:06:59 2016
@author: yxl
"""
import numpy as np
from scipy import ndimage
from sciapp.action import Simple, Filter
from sciapp.object import mark2shp
import pandas as pd

class RegionStatistic(Simple):
    title = 'Intensity Analysis'
    note = ['8-bit', '16-bit', 'int']
    
    para = {'con':'8-connect','inten':None, 'slice':False, 'max':True, 'min':True,'mean':False,
            'center':True, 'var':False,'std':False,'sum':False, 'extent':False, 'labeled':False}
    
    view = [('img', 'inten', 'intensity', ''),
            (list, 'con', ['4-connect', '8-connect'], str, 'conection', 'pix'),
            (bool, 'slice', 'slice'),
            (bool, 'labeled', 'has labeled'),
            ('lab', None, '=========  indecate  ========='),
            (bool, 'center', 'center'),
            (bool, 'extent', 'extent'),
            (bool, 'max', 'max'),
            (bool, 'min', 'min'),
            (bool, 'mean', 'mean'),
            (bool, 'std', 'standard'),
            (bool, 'sum', 'sum')]
            
    #process
    def run(self, ips, imgs, para = None):
        inten = self.app.get_img(para['inten'])
        if not para['slice']:
            imgs = [inten.img]
            msks = [ips.img]
        else: 
            msks = ips.imgs
            imgs = inten.imgs
            if len(msks)==1:
                msks *= len(imgs)
        buf = imgs[0].astype(np.uint32)
        strc = ndimage.generate_binary_structure(2, 1 if para['con']=='4-connect' else 2)
        idct = ['Max','Min','Mean','Variance','Standard','Sum']
        key = {'Max':'max','Min':'min','Mean':'mean',
               'Variance':'var','Standard':'std','Sum':'sum'}
        idct = [i for i in idct if para[key[i]]]
        titles = ['Slice', 'ID'][0 if para['slice'] else 1:] 
        if para['center']: titles.extend(['Center-X','Center-Y'])
        if para['extent']: titles.extend(['Min-Y','Min-X','Max-Y','Max-X'])
        titles.extend(idct)
        k = ips.unit[0]
        data, mark = [],{'type':'layers', 'body':{}}
        # data,mark=[],[]
        for i in range(len(imgs)):
            if para['labeled']:
                n, buf[:] = msks[i].max(), msks[i]
            else: n = ndimage.label(msks[i], strc, output=buf)
            index = range(1, n+1)
            dt = []
            if para['slice']:dt.append([i]*n)
            dt.append(range(n))
            
            xy = ndimage.center_of_mass(buf, buf, index)
            xy = np.array(xy).round(2).T
            if para['center']:dt.extend([xy[1]*k, xy[0]*k])

            boxs = [None] * n
            if para['extent']:
                boxs = ndimage.find_objects(buf)
                boxs = [( i[1].start, i[0].start, i[1].stop-i[1].start,i[0].stop-i[0].start) for i in boxs]
                for j in (0,1,2,3):
                    dt.append([i[j]*k for i in boxs])
            if para['max']:dt.append(ndimage.maximum(imgs[i], buf, index).round(2))
            if para['min']:dt.append(ndimage.minimum(imgs[i], buf, index).round(2))        
            if para['mean']:dt.append(ndimage.mean(imgs[i], buf, index).round(2))
            if para['var']:dt.append(ndimage.variance(imgs[i], buf, index).round(2)) 
            if para['std']:dt.append(ndimage.standard_deviation(imgs[i], buf, index).round(2))
            if para['sum']:dt.append(ndimage.sum(imgs[i], buf, index).round(2))      
 
            layer = {'type':'layer', 'body':[]}
            xy=np.int0(xy).T

            texts = [(i[1],i[0])+('id=%d'%n,) for i,n in zip(xy,range(len(xy)))]
            layer['body'].append({'type':'texts', 'body':texts})
            if para['extent']: layer['body'].append({'type':'rectangles', 'body':boxs})
            mark['body'][i] = layer

            data.extend(list(zip(*dt)))
        self.app.show_table(pd.DataFrame(data, columns=titles), inten.title+'-pixels')
        inten.mark = mark2shp(mark)
        inten.update()

class IntensityFilter(Filter):
    title = 'Intensity Filter'
    note = ['8-bit', '16-bit', 'int', 'auto_msk', 'auto_snap', 'not_slice', 'preview']
    para = {'con':'4-connect', 'inten':None, 'max':0, 'min':0, 'mean':0, 'std':0, 'sum':0, 'front':255, 'back':0}
    view = [('img', 'inten', 'intensity', ''),
            (list, 'con', ['4-connect', '8-connect'], str, 'conection', 'pix'),
            ('lab', None, 'Filter: "+" means >=, "-" means <'),
            (int, 'front', (0, 255), 0, 'front color', ''),
            (int, 'back', (0, 255), 0, 'back color', ''),
            (float, 'mean', (-1e4, 1e4), 1, 'mean', ''),
            (float, 'max',  (-1e4, 1e4), 1, 'max', ''),
            (float, 'min',  (-1e4, 1e4), 1, 'min', ''),
            (float, 'sum',  (-1e6, 1e6), 1, 'sum', ''),
            (float, 'std',  (-1e4, 1e4), 1, 'std', '')]
            
    #process
    def run(self, ips, snap, img, para = None):
        intenimg = self.app.get_img(para['inten']).img
        strc = ndimage.generate_binary_structure(2, 1 if para['con']=='4-connect' else 2)
        buf, n = ndimage.label(snap, strc, output=np.uint32)
        index = range(1, n+1)
        idx = (np.ones(n+1)*para['front']).astype(np.uint8)
        msk = np.ones(n, dtype=np.bool)

        if para['mean']>0: msk *= ndimage.mean(intenimg, buf, index)>=para['mean']
        if para['mean']<0: msk *= ndimage.mean(intenimg, buf, index)<-para['mean']
        if para['max']>0: msk *= ndimage.maximum(intenimg, buf, index)>=para['max']
        if para['max']<0: msk *= ndimage.maximum(intenimg, buf, index)<-para['max']
        if para['min']>0: msk *= ndimage.minimum(intenimg, buf, index)>=para['min']
        if para['min']<0: msk *= ndimage.minimum(intenimg, buf, index)<-para['min']
        if para['sum']>0: msk *= ndimage.sum(intenimg, buf, index)>=para['sum']
        if para['sum']<0: msk *= ndimage.sum(intenimg, buf, index)<-para['sum']
        if para['std']>0: msk *= ndimage.standard_deviation(intenimg, buf, index)>=para['std']
        if para['std']<0: msk *= ndimage.standard_deviation(intenimg, buf, index)<-para['std']

        xy = ndimage.center_of_mass(intenimg, buf, index)
        xy = np.array(xy).round(2).T

        idx[1:][~msk] = para['back']
        idx[0] = 0
        img[:] = idx[buf]

        red_pts = {'type':'points', 'body':xy[::-1].T[~msk], 'color':(255,0,0)}
        green_pts = {'type':'points', 'body':xy[::-1].T[msk], 'color':(0,255,0)}

        self.app.get_img(para['inten']).mark = mark2shp(
            {'type':'layer', 'body':[red_pts, green_pts]})
        self.app.get_img(para['inten']).update()

plgs = [RegionStatistic, IntensityFilter]