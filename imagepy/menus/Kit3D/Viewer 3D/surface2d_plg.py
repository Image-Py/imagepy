# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 22:33:33 2017

@author: yxl
"""
from imagepy import IPy
from imagepy.core.engine import Simple
from scipy.ndimage.filters import gaussian_filter
from imagepy.core import myvi

class Plugin(Simple):
    title = '2D Surface'
    note = ['8-bit', '16-bit']
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

if __name__ == '__main__':
    pass