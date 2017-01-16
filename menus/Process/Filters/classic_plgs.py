# -*- coding: utf-8 -*
import scipy.ndimage as nimg
from core.engines import Filter, Simple

class Gaussian(Filter):
    title = 'Gaussian'
    note = ['all', 'auto_msk', 'auto_snap','preview']

    #parameter
    para = {'sigma':2}
    view = [(float, (0,30), 1,  'sigma', 'sigma', 'pix')]

    #process
    def run(self, ips, img, buf, para = None):
        nimg.gaussian_filter(img, para['sigma'], output=buf)
        
class Gaussian_laplace(Filter):
    title = 'Gaussian Laplace'
    note = ['all', 'auto_msk', 'auto_snap','preview']
    
    #parameter
    para = {'sigma':2}
    view = [(float, (0,30), 1,  'sigma', 'sigma', 'pix')]

    #process
    def run(self, ips, img, buf, para = None):
        nimg.gaussian_laplace(img, para['sigma'], output=buf)
        
class Maximum(Filter):
    title = 'Maximum'
    note = ['all', 'auto_msk', 'auto_snap','preview']
    
    #parameter
    para = {'size':2}
    view = [(float, (0,30), 1,  'size', 'size', 'pix')]

    #process
    def run(self, ips, img, buf, para = None):
        nimg.maximum_filter(img, para['size'], output=buf)

class Minimum(Filter):
    title = 'Minimum'
    note = ['all', 'auto_msk', 'auto_snap','preview']
    
    #parameter
    para = {'size':2}
    view = [(float, (0,30), 1,  'size', 'size', 'pix')]

    #process
    def run(self, ips, img, buf, para = None):
        nimg.minimum_filter(img, para['size'], output=buf)
        
class Median(Filter):
    title = 'Median'
    note = ['all', 'auto_msk', 'auto_snap','preview']
    
    #parameter
    para = {'size':2}
    view = [(float, (0,30), 1,  'size', 'size', 'pix')]

    #process
    def run(self, ips, img, buf, para = None):
        nimg.median_filter(img, para['size'], output=buf)
        
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
    def run(self, ips, img, buf, para = None):
        nimg.sobel(img, output=buf)
        
class Gaussian3D(Simple):
    title = 'Gaussian3D'
    note = ['all', 'stack3d']
    
    #parameter
    para = {'sigma':2}
    view = [(float, (0,30), 1,  'sigma', 'sigma', 'pix')]

    #process
    def run(self, ips, img, para = None):
        nimg.gaussian_filter(img, para['sigma'], output=img)
        
plgs = [Gaussian, Gaussian_laplace,'-', Maximum, Minimum, Median, '-', Prewitt, Sobel, '-', Gaussian3D]