# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 22:33:33 2017

@author: yxl
"""
from imagepy import IPy
from imagepy.core.engine import Simple, Filter, Free
from scipy.ndimage.filters import gaussian_filter
from imagepy.core import myvi

class Show(Free):
    title = 'Show Viewer 3D'
    asyn = False
    def run(self, para):
        myvi.Frame3D.figure(IPy.curapp, title='3D Canvas').Raise()

class Surface2D(Simple):
    title = '2D Surface'
    note = ['8-bit', '16-bit', 'float']
    para = {'name':'undifine', 'scale':2, 'sigma':2,'h':1}
    view = [(str, 'name', 'Name', ''),
            (int, 'scale', (1,5), 0, 'down scale', 'pix'),
            (int, 'sigma', (0,30), 0, 'sigma', ''),
            (float, 'h', (0.1,10), 1, 'scale z', '')]
    
    def load(self, para):
        self.frame = myvi.Frame3D.figure(IPy.curapp, title='3D Canvas')
        return True

    def run(self, ips, imgs, para = None):
        ds, sigma = para['scale'], para['sigma']
        vts, fs, ns, cs = myvi.build_surf2d(ips.img, ds=ds, sigma=para['sigma'], k=para['h'])
        self.frame.viewer.add_surf_asyn(para['name'], vts, fs, ns, cs)
        self.frame.Raise()
        self.frame = None
        #self.frame.add_surf2d('dem', ips.img, ips.lut, scale, sigma)

class Surface3D(Filter):
    modal = False
    title = '3D Surface'
    note = ['8-bit', 'not_slice', 'not_channel', 'preview']
    para = {'name':'undifine', 'ds':2, 'thr':128, 'step':1, 'color':(0,255,0)}
    view = [(str, 'name', 'Name', ''),
            ('slide', 'thr', (0,255), 0, 'threshold'),
            (int, 'ds',   (1,20), 0, 'down scale', 'pix'),
            (int, 'step', (1,20), 0, 'march step', 'pix'),
            ('color', 'color', 'color', 'rgb')]

    def load(self, ips):
        if not ips.is3d:
            IPy.alert('stack3d required!')
            return False
        self.frame = myvi.Frame3D.figure(IPy.curapp, title='3D Canvas')
        self.buflut = ips.lut
        ips.lut = ips.lut.copy()
        return True
    
    def preview(self, ips, para):
        ips.lut[:] = self.buflut
        ips.lut[:para['thr']] = [255,0,0]
        ips.update()

    def run(self, ips, snap, img, para = None):
        imgs = ips.imgs

    def cancel(self, ips):
        ips.lut = self.buflut
        ips.update()

    def run(self, ips, snap, img, para = None):
        ips.lut = self.buflut
        print('------------', para['color'])
        cs = tuple([int(i/255.0) for i in para['color']])
        vts, fs, ns, cs = myvi.build_surf3d(ips.imgs, para['ds'], para['thr'], para['step'], cs)
        self.frame.viewer.add_surf_asyn(para['name'], vts, fs, ns, cs)
        self.frame.Raise()
        self.frame = None

plgs = [Show, Surface2D, Surface3D]
