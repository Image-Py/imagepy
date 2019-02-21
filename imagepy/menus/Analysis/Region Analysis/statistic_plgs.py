# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 01:06:59 2016
@author: yxl
"""
import numpy as np
from scipy import ndimage
import wx

from imagepy import IPy
from imagepy.core.engine import Simple, Filter
from imagepy.core.manager import ImageManager
from imagepy.core.roi.pointroi import PointRoi
import pandas as pd
from imagepy.core.mark import GeometryMark

class Mark:
    def __init__(self, data):
        self.data = data

    def draw(self, dc, f, **key):
        dc.SetPen(wx.Pen((255,255,0), width=1, style=wx.SOLID))
        dc.SetTextForeground((255,255,0))
        font = wx.Font(8, wx.FONTFAMILY_DEFAULT, 
                       wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False)
        
        dc.SetFont(font)
        data = self.data[0 if len(self.data)==0 else key['cur']]

        pos = [f(*(i[0][1], i[0][0])) for i in data]
        for i in pos:dc.DrawCircle(i[0], i[1], 2)

        txts = ['id={}'.format(i) for i in range(len(data))]
        dc.DrawTextList(txts, pos)

        if data[0][1]==None:return
        lt = [f(*(i[1][1], i[1][0])) for i in data]
        rb = [f(*(i[1][3], i[1][2])) for i in data]
        rects = [(x1,y1,x2-x1,y2-y1) for (x1,y1),(x2,y2) in zip(*(lt,rb))]
        dc.DrawRectangleList(rects, brushes = wx.Brush((0,0,0), wx.BRUSHSTYLE_TRANSPARENT))


class RegionStatistic(Simple):
    title = 'Intensity Analysis'
    note = ['8-bit', '16-bit']
    
    para = {'con':'8-connect','inten':None, 'slice':False, 'max':True, 'min':True,'mean':False,
            'center':True, 'var':False,'std':False,'sum':False, 'extent':False}
    
    view = [('img', 'inten', 'intensity', ''),
            (list, 'con', ['4-connect', '8-connect'], str, 'conection', 'pix'),
            (bool, 'slice', 'slice'),
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
        inten = ImageManager.get(para['inten'])
        if not para['slice']:
            imgs = [inten.img]
            msks = [ips.img]
        else: 
            msks = ips.imgs
            imgs = inten.imgs
            if len(msks)==1:
                msks *= len(imgs)
        buf = imgs[0].astype(np.uint16)
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
            n = ndimage.label(msks[i], strc, output=buf)
            index = range(1, n+1)
            dt = []
            if para['slice']:dt.append([i]*n)
            dt.append(range(n))
            
            xy = ndimage.center_of_mass(imgs[i], buf, index)
            xy = np.array(xy).round(2).T
            if para['center']:dt.extend([xy[1]*k, xy[0]*k])

            boxs = [None] * n
            if para['extent']:
                boxs = ndimage.find_objects(buf)
                boxs = [( i[1].start+(i[1].stop-i[1].start)/2, i[0].start+(i[0].stop-i[0].start)/2, i[1].stop-i[1].start,i[0].stop-i[0].start) for i in boxs]
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
        IPy.show_table(pd.DataFrame(data, columns=titles), inten.title+'-pixels')
        inten.mark = GeometryMark(mark)
        inten.update()

class RGMark:
    def __init__(self, data):
        self.xy, self.msk = data

    def draw(self, dc, f, **key):
        dc.SetTextForeground((255,255,0))
        font = wx.Font(8, wx.FONTFAMILY_DEFAULT, 
                       wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False)
        dc.SetFont(font)

        dc.SetPen(wx.Pen((0,255,0), width=1, style=wx.SOLID))
        dc.SetBrush(wx.Brush((0,255,0)))
        pos = [f(*(i[1], i[0])) for i in self.xy[self.msk]]
        for i in pos:dc.DrawCircle(int(i[0]), int(i[1]), 2)


        dc.SetPen(wx.Pen((255,0,0), width=1, style=wx.SOLID))
        dc.SetBrush(wx.Brush((255,0,0)))
        pos = [f(*(i[1], i[0])) for i in self.xy[~self.msk]]
        for i in pos:dc.DrawCircle(int(i[0]), int(i[1]), 2)



class IntensityFilter(Filter):
    title = 'Intensity Filter'
    note = ['8-bit', '16-bit', 'auto_msk', 'auto_snap', 'not_slice', 'preview']
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
        intenimg = ImageManager.get(para['inten']).img
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

        ImageManager.get(para['inten']).mark = RGMark((xy.T, msk))
        ImageManager.get(para['inten']).update()

plgs = [RegionStatistic, IntensityFilter]