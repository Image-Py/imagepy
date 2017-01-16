# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 00:42:18 2017

@author: yxl
"""

from core.engines import Simple
from mayavi import mlab

class Plugin(Simple):
    title = '3D Surface'
    note = ['8-bit', '16-bit', 'stack3d']
    
    para = {'scale':2, 'sigma':2, 'thr':128, 'color':'#00FF00'}
    view = [(int, (1,5), 0, 'down scale', 'scale', 'pix'),
            (int, (0,30), 0, 'sigma', 'sigma', ''),
            ('color', 'color', 'color', 'rgb')]
    
    #process
    def run(self, ips, imgs, para = None):
        volume = mlab.pipeline.scalar_field(ips.imgs)
        if para['sigma']!=0:
            volume = mlab.pipeline.user_defined(volume, filter='ImageGaussianSmooth')
            volume.filter.standard_deviations = [para['sigma']]*3
        c = tuple([i/255.0 for i in para['color']])
        contour = mlab.pipeline.iso_surface(volume, contours=[para['thr']], color=c)
        mlab.show()

if __name__ == '__main__':
    pass