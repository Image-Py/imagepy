# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 20:34:59 2016
@author: yxl
"""
from imagepy import IPy, root_dir
import wx, numpy as np, os
from imagepy.core.engine import Simple
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
        print(ips.imgtype, ips.imgtype == '8-bit')
        if ips.imgtype == 'rgb':
            hist = [np.histogram(ips.img[:,:,i], np.arange(257))[0] for i in (0,1,2)]
        else:
            hist = np.histogram(ips.lookup(), np.arange(257))[0]
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
                self.progress(n, len(imgs))
        else: data = [self.count(ips.img, para)]
        IPy.table(ips.title+'-statistic', data, titles)
        
plgs = [Frequence, Statistic, Histogram]