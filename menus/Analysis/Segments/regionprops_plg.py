# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 01:06:59 2016
@author: yxl
"""
from imagepy import IPy, wx
import numpy as np
from imagepy.core.engine import Simple
from imagepy.core.manager import WindowsManager
from scipy.ndimage import label
from skimage.measure import regionprops

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
        for i in range(len(data)):
            pos = f(*(data[i][0][1], data[i][0][0]))
            dc.DrawCircle(pos[0], pos[1], 2)
            dc.DrawText('id={}'.format(i), pos[0], pos[1])
            if data[i][1]==None:continue
            k1, k2, a = data[i][1]
            aixs = np.array([[-np.sin(a), np.cos(a)],
                             [np.cos(a), np.sin(a)]])*[k1/2, k2/2]
            ar = np.linspace(0, np.pi*2,25)
            xy = np.vstack((np.cos(ar), np.sin(ar)))
            arr = np.dot(aixs, xy).T+data[i][0]
            dc.DrawLines([f(*i) for i in arr[:,::-1]])

# center, area, l, extent, cov
class Plugin(Simple):
    title = 'Region Props'
    note = ['8-bit', '16-bit']
    para = {'img':None, 'center':True, 'area':True, 'l':True, 'extent':False, 'cov':False, 'slice':False}
    view = [('img', 'label', 'img', ''),
            (bool, 'center', 'center'),
            (bool, 'area', 'area'),
            (bool, 'l', 'l'),
            (bool, 'extent', 'extent'),
            (bool, 'cov', 'cov'),
            (bool, 'slice', 'slice')]

    #process
    def run(self, ips, imgs, para = None):
        if not para['slice']:
            msks = [ips.img]
            imgs = [WindowsManager.get(para['img']).ips.img]
        else: 
            msks = imgs
            imgs = WindowsManager.get(para['img']).ips.imgs

        titles = ['Slice', 'ID'][0 if para['slice'] else 1:]
        if para['center']:titles.extend(['Center-X','Center-Y'])
        if para['area']:titles.append('Area')
        if para['l']:titles.append('Perimeter')
        if para['extent']:titles.extend(['Min-Y','Min-X','Max-Y','Max-X'])
        if para['cov']:titles.extend(['Major','Minor','Ori'])
        buf = imgs[0].astype(np.uint16)
        data, mark = [], []
        strc = np.array([[0,1,0],[1,1,1],[0,1,0]], dtype=np.uint8)
        for i in range(len(imgs)):
            label(msks[i], strc, output=buf)
            ls = regionprops(buf, imgs[i])

            dt = [[i]*len(ls), list(range(len(ls)))]
            if not para['slice']:dt = dt[1:]

            if not para['cov']: cvs = [None] * len(ls)
            else: cvs = [(i.major_axis_length, i.minor_axis_length, i.orientation) for i in ls]
            centroids = [i.centroid for i in ls]
            mark.append([(center, cov) for center,cov in zip(centroids, cvs)])
            if para['center']:
                dt.append([round(i.centroid[0],1) for i in ls])
                dt.append([round(i.centroid[1],1) for i in ls])
            if para['area']:
                dt.append([i.area for i in ls])
            if para['l']:
                dt.append([round(i.perimeter,1) for i in ls])
            if para['extent']:
                for j in (0,1,2,3):
                    dt.append([i.bbox[j] for i in ls])
            if para['cov']:
                dt.append([round(i.major_axis_length, 1) for i in ls])
                dt.append([round(i.minor_axis_length, 1) for i in ls])
                dt.append([round(i.orientation, 1) for i in ls])

            data.extend(list(zip(*dt)))
        ips.mark = Mark(mark)
        IPy.table(ips.title+'-region', data, titles)