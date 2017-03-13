# -*- coding: utf-8 -*
import scipy.ndimage as nimg
from core.engines import Filter, Simple
import numpy as np

class Gaussian(Filter):
    title = 'Gaussian'
    note = ['all', 'auto_msk', 'auto_snap','preview']

    #parameter
    para = {'sigma':2}
    view = [(float, (0,30), 1,  'sigma', 'sigma', 'pix')]

    #process
    def run(self, ips, snap, img, para = None):
        nimg.gaussian_filter(snap, para['sigma'], output=img)
        
class Gaussian_laplace(Filter):
    title = 'Gaussian Laplace'
    note = ['all', 'auto_msk', 'auto_snap','preview']
    
    #parameter
    para = {'sigma':2}
    view = [(float, (0,30), 1,  'sigma', 'sigma', 'pix')]

    #process
    def run(self, ips, snap, img, para = None):
        nimg.gaussian_laplace(snap, para['sigma'], output=img)
        
class Maximum(Filter):
    title = 'Maximum'
    note = ['all', 'auto_msk', 'auto_snap','preview']
    
    #parameter
    para = {'size':2}
    view = [(float, (0,30), 1,  'size', 'size', 'pix')]

    #process
    def run(self, ips, snap, img, para = None):
        nimg.maximum_filter(snap, para['size'], output=img)

class Minimum(Filter):
    title = 'Minimum'
    note = ['all', 'auto_msk', 'auto_snap','preview']
    
    #parameter
    para = {'size':2}
    view = [(float, (0,30), 1,  'size', 'size', 'pix')]

    #process
    def run(self, ips, snap, img, para = None):
        nimg.minimum_filter(snap, para['size'], output=img)
        
class Median(Filter):
    title = 'Median'
    note = ['all', 'auto_msk', 'auto_snap','preview']
    
    #parameter
    para = {'size':2}
    view = [(int, (0,30), 0,  'size', 'size', 'pix')]

    #process
    def run(self, ips, snap, img, para = None):
        nimg.median_filter(snap, para['size'], output=img)
        
class Prewitt(Filter):
    title = 'Prewitt'
    note = ['all', 'auto_msk', 'auto_snap','preview']

    #process
    def run(self, ips, img, buf, para = None):
        nimg.prewitt(img, output=buf)
        
class Sobel(Filter):
    title = 'Sobel'
    note = ['all', 'auto_msk', 'auto_snap','preview']

    #process
    def run(self, ips, snap, img, para = None):
        nimg.sobel(snap, output=img)
        
class USM(Filter):
    title = 'Unsharp Mask'
    note = ['all', 'auto_msk', 'auto_snap', '2int', 'preview']

    #parameter
    para = {'sigma':2, 'weight':0.5}
    view = [(float, (0,30), 1,  'sigma', 'sigma', 'pix'),
            (float, (0,5), 1,  'weight', 'weight', '')]

    #process
    def run(self, ips, snap, img, para = None):
        print 'haha'
        nimg.gaussian_filter(snap, para['sigma'], output=img)
        img -= snap
        np.multiply(img, -para['weight'], out=img, casting='unsafe')
        img += snap
        
        
class Gaussian3D(Simple):
    title = 'Gaussian3D'
    note = ['all', 'stack3d']
    
    #parameter
    para = {'sigma':2}
    view = [(float, (0,30), 1,  'sigma', 'sigma', 'pix')]

    #process
    def run(self, ips, img, para = None):
        nimg.gaussian_filter(img, para['sigma'], output=img)
        
plgs = [Gaussian, Gaussian_laplace,'-', Maximum, Minimum, Median, '-', Prewitt, Sobel, '-', USM, '-', Gaussian3D]