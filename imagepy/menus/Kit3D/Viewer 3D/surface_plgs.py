# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 22:33:33 2017

@author: yxl
"""
from sciapp.action import Simple, Filter, Free
from scipy.ndimage.filters import gaussian_filter
from sciapp.object import Surface, MarkText
from sciapp.util import surfutil

class Show(Free):
    title = 'Show Viewer 3D'
    def run(self, para):
        self.app.show_mesh()

class Surface2D(Simple):
    title = '2D Surface'
    note = ['8-bit', '16-bit', 'float']
    para = {'name':'undifine', 'scale':2, 'sigma':2,'h':1}
    view = [(str, 'name', 'Name', ''),
            (int, 'scale', (1,5), 0, 'down scale', 'pix'),
            (int, 'sigma', (0,30), 0, 'sigma', ''),
            (float, 'h', (0.1,10), 1, 'scale z', '')]

    def run(self, ips, imgs, para = None):
        ds, sigma = para['scale'], para['sigma']
        vts, fs, ns, cs = surfutil.build_surf2d(ips.img, ds=ds, sigma=para['sigma'], k=para['h'])
        self.app.show_mesh(Surface(vts, fs, ns, cs), para['name'])

class Surface3D(Simple):
    modal = False
    title = '3D Surface'
    note = ['8-bit', 'stack3d', 'preview']
    para = {'name':'undifine', 'ds':2, 'thr':128, 'step':1, 'color':(0,255,0)}
    view = [(str, 'name', 'Name', ''),
            ('slide', 'thr', (0,255), 0, 'threshold'),
            (int, 'ds',   (1,20), 0, 'down scale', 'pix'),
            (int, 'step', (1,20), 0, 'march step', 'pix'),
            ('color', 'color', 'color', 'rgb')]

    def load(self, ips):
        self.buflut = ips.lut
        ips.lut = ips.lut.copy()
        return True
    
    def preview(self, ips, para):
        ips.lut[:] = self.buflut
        ips.lut[:para['thr']] = [255,0,0]

    def cancel(self, ips):
        ips.lut = self.buflut

    def run(self, ips, imgs, para = None):
        ips.lut = self.buflut
        cs = tuple([int(i/255.0) for i in para['color']])
        vts, fs, ns, cs = surfutil.build_surf3d(ips.imgs, para['ds'], para['thr'], para['step'], cs)
        self.app.show_mesh(Surface(vts, fs, ns, cs), para['name'])

class ImageCube(Simple):
    modal = False
    title = '3D Image Cube'
    note = ['8-bit', 'rgb', 'stack3d']
    para = {'name':'undifine', 'ds':1, 'color':(0,255,0), 'surface':True, 'box':False}
    view = [(str, 'name', 'Name', 'xxx-surface'),
            (bool, 'surface', 'show surface'),
            (int, 'ds', (1,20), 0, 'down scale', 'pix'),
            (bool, 'box', 'show box'),
            ('color', 'color', 'box color', 'rgb')]

    def run(self, ips, imgs, para = None):
        if para['surface']:
            vts, fs, ns, cs = surfutil.build_img_cube(imgs, para['ds'])
            self.app.show_mesh(Surface(vts, fs, ns, cs), para['name']+'-surface')
        if para['box']:
            vts, fs, ns, cs = surfutil.build_img_box(imgs, para['color'])
            self.app.show_mesh(Surface(vts, fs, ns, cs, mode='grid'), para['name']+'-box')

plgs = [Show, Surface2D, Surface3D, ImageCube]
