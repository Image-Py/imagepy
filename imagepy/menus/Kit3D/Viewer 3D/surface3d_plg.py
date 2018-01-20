# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 00:42:18 2017

@author: yxl
"""
from imagepy.core.engine import Filter
from imagepy import IPy
from imagepy.core import myvi
import numpy as np

class Plugin(Filter):
    modal = False
    title = '3D Surface'
    note = ['8-bit', 'not_slice', 'not_channel', 'preview']
    para = {'name':'undifine', 'ds':2, 'thr':128, 'step':1, 'color':(0,255,0)}
    view = [(str, 'Name', 'name',''),
            ('slide', (0,255), 'threshold', 'thr', ''),
            (int, (1,20), 0, 'down scale', 'ds', 'pix'),
            (int, (1,20), 0, 'march step', 'step', 'pix'),
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
        ips.update = 'pix'

    def run(self, ips, snap, img, para = None):
        imgs = ips.imgs

    def cancel(self, ips):
        ips.lut = self.buflut
        ips.update = 'pix'

    def run(self, ips, snap, img, para = None):
        ips.lut = self.buflut
        print('------------', para['color'])
        cs = tuple([int(i/255.0) for i in para['color']])
        vts, fs, ns, cs = myvi.build_surf3d(ips.imgs, para['ds'], para['thr'], para['step'], cs)
        self.frame.viewer.add_surf_asyn(para['name'], vts, fs, ns, cs)
        self.frame.Raise()
        self.frame = None


    '''
    def run(self, ips, imgs, para = None):
        from mayavi import mlab
        volume = mlab.pipeline.scalar_field(ips.imgs)
        if para['sigma']!=0:
            volume = mlab.pipeline.user_defined(volume, filter='ImageGaussianSmooth')
            volume.filter.standard_deviations = [para['sigma']]*3
        c = tuple([i/255.0 for i in para['color']])
        contour = mlab.pipeline.iso_surface(volume, contours=[para['thr']], 
                                            color=c, opacity=para['opa'])
        mlab.show()
    '''
if __name__ == '__main__':
    pass