# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 22:33:33 2017

@author: yxl
"""
from sciapp.action import Simple, Filter, Free
from scipy.ndimage.filters import gaussian_filter
from sciapp.object import Mesh, Scene, Surface2d, Surface3d, Volume3d
from imagepy.app import ColorManager
from sciapp.util import meshutil

class Show(Free):
    title = 'Show Viewer 3D'
    para = {'name':'Scene', 'bg':(0,0,0)}
    view = [(str, 'name', 'name', ''),
            ('color', 'bg', 'background', 'color')]

    def run(self, para):
        scene = Scene(bg_color=[i/255 for i in para['bg']])
        self.app.show_mesh(scene, para['name'])

class Surface2D(Simple):
    title = '2D Surface'
    note = ['8-bit', '16-bit', 'float']
    para = {'name':'undifine', 'sample':2, 'sigma':2,'h':0.3, 'cm':'gray'}
    view = [(str, 'name', 'Name', ''),
            (int, 'sample', (1,10), 0, 'down sample', 'pix'),
            (int, 'sigma', (0,30), 0, 'sigma', ''),
            (float, 'h', (0.1,10), 1, 'scale z', ''),
            ('cmap', 'cm', 'color map')]

    def run(self, ips, imgs, para = None):
        ds, sigma, cm = para['sample'], para['sigma'], ColorManager.get(para['cm'])
        mesh = Surface2d(ips.img, sample=ds, sigma=sigma, k=para['h'], cmap=cm)
        self.app.show_mesh(mesh, para['name'])

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
        surf3d = Surface3d(imgs=ips.imgs, level=para['thr'], sample=para['ds'], step=para['step'], colors=cs)
        self.app.show_mesh(surf3d, para['name'])

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

class Volume3D(Simple):
    modal = False
    title = '3D Volume'
    note = ['8-bit', 'stack3d']
    para = {'name':'undifine', 'step':1, 'cm':'gray', 'cube':True}
    view = [(str, 'name', 'Name', ''),
            (int, 'step', (1,10), 0, 'march step', 'pix'),
            ('cmap', 'cm', 'color map'),
            (bool, 'cube', 'draw outline cube')]

    def run(self, ips, imgs, para = None):
        cmap =  ColorManager.get(para['cm'])
        self.app.show_mesh(Volume3d(imgs, step=para['step'], cmap=cmap), para['name'])
        if para['cube']:
            vts, fs = meshutil.create_bound((0,0,0), imgs.shape)
            self.app.show_mesh(Mesh(verts=vts, faces=fs, colors=(1,1,1), mode='grid'), 'box')

plgs = [Show, Surface2D, Surface3D, ImageCube, Volume3D]
