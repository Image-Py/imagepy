# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 22:05:43 2016
@author: yxl
"""
import numpy as np
from scipy.ndimage import label, generate_binary_structure
from skimage.segmentation import find_boundaries
from sciapp.action import Filter, Simple
from imagepy.ipyalg.graph import connect, render
from sciapp.object import Image

class Label(Simple):
    title = 'Label Image'
    note = ['8-bit', '16-bit']    
    para = {'slice':False, 'con':'4-Connect'}
    view = [(list, 'con', ['4-Connect','8-Connect'], str, 'Structure', 'connect'),
            (bool, 'slice', 'slice')]
        
    def run(self, ips, imgs, para = None):
        if not para['slice']:  imgs = [ips.img]
        labels = []
        for i in range(len(imgs)):
            self.progress(i, len(imgs))
            con = 1 if para['con']=='4-Connect' else 2
            strc = generate_binary_structure(2, con)
            lab, n = label(imgs[i], strc, output = np.int32)
            labels.append(lab)
        self.app.show_img(labels, ips.title+'-label') 

class Boundaries(Simple):
    title = 'Mark Boundaries'
    note = ['8-bit', '16-bit','int']    
    para = {'slice':False, 'mode':'outer', 'con':'4-Connect'}
    view = [(list, 'con', ['4-Connect','8-Connect'], str, 'structure', 'connect'),
            (list, 'mode', ['thick', 'inner', 'outer', 'subpixel'], str, 'mode', ''),
            (bool, 'slice', 'slice')]
        
    def run(self, ips, imgs, para = None):
        if not para['slice']:  imgs = [ips.img]
        labels = []
        for i in range(len(imgs)):
            self.progress(i, len(imgs))
            con = 1 if para['con']=='4-Connect' else 2
            bound = find_boundaries(imgs[i], con, para['mode'])
            bound.dtype = np.uint8
            bound *= 255
            labels.append(bound)
        self.app.show_img(labels, ips.title+'-boundary') 

class Render(Simple):
    title = 'Label Render'
    note = ['8-bit', '16-bit', 'int']    
    para = {'slice':False, 'con':'8-Connect', 'colors':6, 'back':False}
    view = [(list, 'con', ['4-Connect','8-Connect'], str, 'structure', 'connect'),
            (int, 'colors', (4, 255), 0, 'colors', 'n'),
            (bool, 'back', 'background'),
            (bool, 'slice', 'slice')]
    
    def run(self, ips, imgs, para = None):
        if not para['slice']:  imgs = [ips.img]
        labels = []
        for i in range(len(imgs)):
            self.progress(i, len(imgs))
            con = 1 if para['con']=='4-Connect' else 2
            idx = connect.connect_graph(imgs[i], con, para['back'])
            idx = connect.mapidx(idx)
            cmap = render.node_render(idx, para['colors'], 10)

            lut = np.ones(imgs[i].max()+1, dtype=np.uint8)
            lut[0] = 0
            for j in cmap: lut[j] = cmap[j]
            labels.append(lut[imgs[i]])

        ips = Image(labels, ips.title+'-render')
        ips.range = (0, para['colors'])
        self.app.show_img(ips) 

plgs = [Label, Boundaries, Render]