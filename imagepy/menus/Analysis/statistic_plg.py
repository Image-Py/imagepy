# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 20:34:59 2016
@author: yxl
"""
from imagepy import IPy, root_dir
import wx, numpy as np, os
from imagepy.core.engine import Simple
from imagepy.core.roi import PointRoi
from imagepy.core.manager import WindowsManager
from imagepy.ui.widgets import HistCanvas
from wx.lib.pubsub import pub

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
            histc = HistCanvas(panel)
            histc.set_hist(hist[i])
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
        histc = HistCanvas(panel)
        histc.set_hist(hist)
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
    note = ['8-bit', '16-bit', 'rgb']

    def run(self, ips, imgs, para = None):
        msk = ips.get_msk('in')
        if ips.imgtype == 'rgb':
            img = ips.img if msk is None else ips.img[msk]
            hist = [np.histogram(img[:,i], np.arange(257))[0] for i in (0,1,2)]
        else:
            img = ips.lookup() if msk is None else ips.lookup()[msk]
            hist = np.histogram(img, np.arange(257))[0]
        show_hist(WindowsManager.get(), ips.title+'-Histogram', hist)


class Frequence(Simple):
    title = 'Frequence'
    note = ['8-bit', '16-bit']
    
    para = {'fre':True, 'slice':False}
    view = [(bool, 'count frequence', 'fre'),
            (bool, 'each slices', 'slice')]
        
    def run(self, ips, imgs, para = None):
        if not para['slice']: imgs = [ips.img]
        data = []
        msk = ips.get_msk('in')
        for i in range(len(imgs)):
            img = imgs[i] if msk is None else imgs[i][msk]
            maxv = img.max()
            if maxv==0:continue
            ct = np.histogram(img, maxv, [1,maxv+1])[0]
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
    title = 'Pixel Statistic'
    note = ['8-bit', '16-bit', 'int', 'float']
    
    para = {'max':True, 'min':True,'mean':False,'var':False,'std':False,'slice':False}
    view = [(bool, 'Max', 'max'),
            (bool, 'Min', 'min'),
            (bool, 'Mean', 'mean'),
            (bool, 'Variance', 'var'),
            (bool, 'Standard', 'std'),
            (bool, 'slice', 'slice')]
        
    def count(self, img, para):
        rst = []
        if para['max']: rst.append(img.max())
        if para['min']: rst.append(img.min())
        if para['mean']: rst.append(img.mean().round(2))
        if para['var']: rst.append(img.var().round(2))
        if para['std']: rst.append(img.std().round(2))
        return rst
        
    def run(self, ips, imgs, para = None):
        titles = ['Max','Min','Mean','Variance','Standard']
        key = {'Max':'max','Min':'min','Mean':'mean','Variance':'var','Standard':'std'}
        titles = [i for i in titles if para[key[i]]]

        if not self.para['slice']:imgs = [ips.img]
        data = []
        msk = ips.get_msk('in')
        for n in range(len(imgs)):
            img = imgs[n] if msk is None else imgs[n][msk]
            data.append(self.count(img, para))
            self.progress(n, len(imgs))
        IPy.table(ips.title+'-statistic', data, titles)
        
class Mark:
    def __init__(self, data):
        self.data = data

    def draw(self, dc, f, **key):
        dc.SetPen(wx.Pen((255,255,0), width=1, style=wx.SOLID))
        dc.SetTextForeground((255,255,0))
        font = wx.Font(8, wx.FONTFAMILY_DEFAULT, 
                       wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False)
        
        dc.SetFont(font)
        data = self.data[0 if len(self.data)==1 else key['cur']]

        for i in range(len(data)):
            pos = f(*(data[i][0], data[i][1]))
            dc.SetBrush(wx.Brush((255,255,255)))
            dc.DrawCircle(pos[0], pos[1], 2)
            dc.SetBrush(wx.Brush((0,0,0), wx.BRUSHSTYLE_TRANSPARENT))
            dc.DrawCircle(pos[0], pos[1], data[i][2]*key['k'])
            dc.DrawText('id={}, r={}'.format(i, data[i][2]), pos[0], pos[1])

class PointsValue(Simple):
    title = 'Points Value'
    note = ['8-bit', '16-bit', 'req_roi']
    
    para = {'buf':False, 'slice':False}
    view = [(bool, 'buffer by the value', 'buf'),
            (bool, 'slice', 'slice')]
        
    def load(self, ips):
        if not isinstance(ips.roi, PointRoi):
            IPy.alert('a PointRoi needed!')
            return False
        return True
    
        
    def run(self, ips, imgs, para = None):
        titles = ['SliceID', 'X', 'Y', 'Value']
        k, u = ips.unit
        if not para['slice']:
            imgs = [ips.img]
            titles = titles[1:]
        data, mark = [], []
        pts = np.array(ips.roi.body).round().astype(np.int)
        for n in range(len(imgs)):
            xs, ys = (pts.T*k).round(2)
            vs = imgs[n][ys, xs]
            cont = ([n]*len(vs), xs, ys, vs.round(2))
            if not para['slice']: cont = cont[1:]
            data.extend(zip(*cont))
            if para['buf']:mark.append(list(zip(xs, ys, vs.round(2))))
            self.progress(n, len(imgs))
        IPy.table(ips.title+'-points', data, titles)
        if para['buf']:ips.mark = Mark(mark)

plgs = [Frequence, Statistic, Histogram, PointsValue]