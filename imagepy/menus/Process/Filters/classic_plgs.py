# -*- coding: utf-8 -*
import scipy.ndimage as nimg
from imagepy.core.engine import Filter, Simple
import numpy as np

class Gaussian(Filter):
    """Gaussian: derived from imagepy.core.engine.Filter """
    title = 'Gaussian'
    note = ['all', 'auto_msk', 'auto_snap','preview']
    para = {'sigma':2}
    view = [(float, (0,30), 1,  'sigma', 'sigma', 'pix')]
    
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
    note = ['all', '2int', 'auto_msk', 'auto_snap','preview']
    para = {'axis':'horizontal'}
    view = [(list, ['horizontal', 'vertical'], str, 'direction', 'axis', 'aixs')]

    #process
    def run(self, ips, snap, img, para = None):
        nimg.prewitt(snap, axis={'horizontal':0,'vertical':1}[para['axis']], output=img)
        
class Sobel(Filter):
    title = 'Sobel'
    note = ['all', '2int', 'auto_msk', 'auto_snap','preview']
    para = {'axis':'horizontal'}
    view = [(list, ['horizontal', 'vertical'], str, 'direction', 'axis', 'aixs')]
    #process
    def run(self, ips, snap, img, para = None):
        nimg.sobel(snap, axis={'horizontal':0,'vertical':1}[para['axis']], output=img)
        
class USM(Filter):
    title = 'Unsharp Mask'
    note = ['all', 'auto_msk', 'auto_snap', '2int', 'preview']

    #parameter
    para = {'sigma':2, 'weight':0.5}
    view = [(float, (0,30), 1,  'sigma', 'sigma', 'pix'),
            (float, (0,5), 1,  'weight', 'weight', '')]

    #process
    def run(self, ips, snap, img, para = None):
        print('USM runing...')
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