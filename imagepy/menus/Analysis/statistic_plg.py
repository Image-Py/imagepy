# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 20:34:59 2016
@author: yxl
"""
from imagepy import root_dir
import wx, numpy as np, os
from sciapp.action import Filter,Simple
from pubsub import pub
import pandas as pd

from skimage.graph import route_through_array
from sciapp.object import mark2shp, Circles
from sciwx.widgets.histpanel import HistPanel

class HistogramFrame(wx.Frame):
    def __init__(self, parent, title, hist):
        wx.Frame.__init__(self, parent, title=title, style = wx.DEFAULT_DIALOG_STYLE)
        logopath = os.path.join(root_dir, 'data/logo.ico')
        self.SetIcon(wx.Icon(logopath, wx.BITMAP_TYPE_ICO))
        if len(hist)==3:self.rgb(hist)
        else: self.gray(hist)

    def rgb(self, hist):
        panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        back = wx.BoxSizer( wx.VERTICAL )
        back.Add(panel, 1, wx.EXPAND)
        sizer = wx.BoxSizer( wx.VERTICAL )
        rgb = ['Red', 'Green', 'Blue']
        for i in (0,1,2):
            histc = HistPanel(panel)
            histc.SetValue(hist[i])
            txt = wx.StaticText( panel, wx.ID_ANY, 'Channel:'+ rgb[i], wx.DefaultPosition, wx.DefaultSize, 0 )
            sizer.Add( txt, 0, wx.LEFT|wx.RIGHT, 8 )
            sizer.Add( histc, 0, wx.LEFT|wx.RIGHT, 8 )
            mean, lim = np.dot(hist[i], range(256))/hist[i].sum(), np.where(hist[i]>0)[0]
            sta = 'Statistic:   Mean:%s   Min:%s   Max:%s'%(mean.round(1), lim.min(), lim.max())
            txt = wx.StaticText( panel, wx.ID_ANY, sta, wx.DefaultPosition, wx.DefaultSize, 0 )
            sizer.Add( txt, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 8 )
        panel.SetSizer( sizer )
        self.SetSizer(back)
        self.Fit()

    def gray(self, hist):
        panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        back = wx.BoxSizer( wx.VERTICAL )
        back.Add(panel, 1, wx.EXPAND)
        sizer = wx.BoxSizer( wx.VERTICAL )
        histc = HistPanel(panel)
        histc.SetValue(hist)
        txt = wx.StaticText( panel, wx.ID_ANY, 'Channel:'+'Gray', wx.DefaultPosition, wx.DefaultSize, 0 )
        sizer.Add( txt, 0, wx.LEFT|wx.RIGHT, 8 )
        sizer.Add( histc, 0, wx.LEFT|wx.RIGHT, 8 )
        mean, lim = np.dot(hist, range(256))/hist.sum(), np.where(hist>0)[0]
        sta = 'Statistic:   Mean:%s   Min:%s   Max:%s'%(mean.round(1), lim.min(), lim.max())
        txt = wx.StaticText( panel, wx.ID_ANY, sta, wx.DefaultPosition, wx.DefaultSize, 0 )
        sizer.Add( txt, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 8 )
        panel.SetSizer( sizer )
        self.SetSizer(back)
        self.Fit()

def showhist(parent, title, hist):
    HistogramFrame(parent, title, hist).Show()

pub.subscribe(showhist, 'showhist')
def show_hist(parent, title, hist):
    wx.CallAfter(pub.sendMessage, 'showhist', parent=parent, title=title, hist=hist) 

class Histogram(Simple):
    title = 'Histogram'
    note = ['all']

    def run(self, ips, imgs, para = None):
        msk = ips.mask('in')
        rg = np.linspace(*ips.range, 257)
        img = ips.img if msk is None else ips.img[msk]
        if ips.channels == 3:
            hist = [np.histogram(img.ravel()[i::3], rg)[0] for i in (0,1,2)]
        else: hist = np.histogram(img,rg)[0]
        show_hist(self.app, ips.title+'-Histogram', hist)

class Frequence(Simple):
    title = 'Frequence'
    note = ['8-bit', '16-bit']
    
    para = {'fre':True, 'slice':False}
    view = [(bool, 'fre', 'count frequence'),
            (bool, 'slice', 'slice')]
        
    def run(self, ips, imgs, para = None):
        if not para['slice']: imgs = [ips.img]
        data = []
        msk = ips.mask('in')
        for i in range(len(imgs)):
            img = imgs[i] if msk is None else imgs[i][msk]
            ct = np.bincount(img.ravel()) #np.histogram(img, maxv+1, [0,maxv])[0]
            titles = ['slice','value','count']
            dt = [np.ones(len(ct), dtype=np.uint32)+i, np.arange(len(ct)), ct]
            if not para['slice']:
                titles, dt = titles[1:], dt[1:]
            if self.para['fre']:
                fre = ct/float(ct.sum())
                titles.append('frequence')
                dt.append(fre.round(4))
            dt = list(zip(*dt))
            data.extend(dt)

        self.app.show_table(pd.DataFrame(data, columns=titles), ips.title+'-histogram')
        
class Statistic(Simple):
    title = 'Pixel Statistic'
    note = ['all']
    
    para = {'max':True, 'min':True,'mean':False,'var':False,'std':False,'slice':False}
    view = [(bool, 'max', 'max'),
            (bool, 'min', 'min'),
            (bool, 'mean', 'mean'),
            (bool, 'var', 'variance'),
            (bool, 'std', 'standard'),
            (bool, 'slice', 'slice')]
        
    def count(self, img, para):
        rst = []
        if para['max']: rst.append(img.max())
        if para['min']: rst.append(img.min())
        if para['mean']: rst.append(img.mean())
        if para['var']: rst.append(img.var())
        if para['std']: rst.append(img.std())
        return rst
        
    def run(self, ips, imgs, para = None):
        titles = ['Max','Min','Mean','Variance','Standard']
        key = {'Max':'max','Min':'min','Mean':'mean','Variance':'var','Standard':'std'}
        titles = [i for i in titles if para[key[i]]]

        if not self.para['slice']:imgs = [ips.img]
        data = []
        msk = ips.mask('in')
        for n in range(len(imgs)):
            img = imgs[n] if msk is None else imgs[n][msk]
            data.append(self.count(img, para))
            self.progress(n, len(imgs))
        self.app.show_table(pd.DataFrame(data, columns=titles), ips.title+'-statistic')

class PointsValue(Simple):
    title = 'Points Value'
    note = ['8-bit', '16-bit', 'req_roi']
    
    para = {'buf':False, 'slice':False}
    view = [(bool, 'buf', 'buffer by the value'),
            (bool, 'slice', 'slice')]
        
    def load(self, ips):
        if ips.roi.roitype != 'point' and ips.roi.roitype != 'points':
            return self.app.alert('a PointRoi needed!')
        return True
    
        
    def run(self, ips, imgs, para = None):
        titles = ['SliceID', 'X', 'Y', 'Value']
        k, u = ips.unit
        if not para['slice']:
            imgs = [ips.img]
            titles = titles[1:]
        data = []
        pts = np.vstack([i.body.reshape(-1,2) for i in ips.roi.body])
        layers = {'type':'layers', 'body':{}}
        for n in range(len(imgs)):
            xs, ys = (pts.T[:2]*k).round(2).astype(np.int16)
            vs = imgs[n][ys, xs]
            cont = ([n]*len(vs), xs, ys, vs.round(2))
            if not para['slice']: cont = cont[1:]
            data.extend(zip(*cont))
            if para['buf']:
                layers['body'][n] = {'type':'circles', 'body':list(zip(xs, ys, vs.round(2)))}
            self.progress(n, len(imgs))
        self.app.show_table(pd.DataFrame(data, columns=titles), ips.title+'-points')
        if para['buf']:ips.mark = mark2shp(layers)

class ShortRoute(Filter):
    title = 'Shortest Route'
    note = ['auto_snap','8-bit', '16-bit','int', 'float', 'req_roi', '2int', 'preview']
    
    para = {'fully connected':True, 'lcost':0, 'max':False, 'geometric':True, 'type':'white line'}
    view = [(float, 'lcost', (0, 1e5), 3, 'step', 'cost'),
            (bool, 'max', 'max cost'),
            (bool, 'fully connected', 'fully connected'),
            (bool, 'geometric', 'geometric'),
            (list, 'type', ['white line', 'gray line', 'white line on ori'], str, 'output', '')]
        
    def load(self, ips):
        if ips.roi.roitype != 'line':
            return self.app.alert('LineRoi are needed!')
        return True

    def run(self, ips, snap, img, para = None):
        img[:] = snap
        if para['max']: img *= -1
        np.add(img, para['lcost']-img.min(), casting='unsafe', out=img)

        minv, maxv = ips.range
        routes = []
        for line in ips.roi.body:
            pts = np.array(list(zip(line.body[:-1], line.body[1:])))
            for p0, p1 in pts[:,:,::-1].astype(int):
                indices, weight = route_through_array(img, p0, p1)
                routes.append(indices)
        rs, cs = np.vstack(routes).T
        if para['type']=='white line on ori':
            img[:] = snap
            img[rs,cs] = maxv
        elif para['type']=='gray line':
            img[:] = minv
            img[rs,cs] = snap[rs,cs]
        elif para['type']=='white line':
            img[:] = minv
            img[rs,cs] = maxv
        
plgs = [Frequence, Statistic, Histogram, PointsValue,ShortRoute]