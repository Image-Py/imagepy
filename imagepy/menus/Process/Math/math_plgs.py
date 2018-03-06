# -*- coding: utf-8 -*
import numpy as np
from imagepy.core.engine import Filter

class Add(Filter):
    """Add_plg: derived from imagepy.core.engine.Filter """
    title = 'Add'
    note = ['all', 'auto_msk', 'auto_snap', 'preview', '2int']
    para = {'num':0}
    view = [('slide', (-100, 100), '-100', 'num', '+100')]
    
    def run(self, ips, snap, img, para = None):
        np.add(snap, para['num'], out=img, casting='unsafe')
        
class Multiply(Filter):
    """Multiply_plg: derived from imagepy.core.engine.Filter """
    title = 'Multiply'
    note = ['all', 'auto_msk', 'auto_snap', 'preview', '2int']
    para = {'num':0}
    view = [(float, (-100,100), 2, '-100', 'num', '+100')]
    
    def run(self, ips, snap, img, para = None):
        np.multiply(snap, para['num'], out=img, casting='unsafe')
        
class Max(Filter):
    """Max_plg: derived from imagepy.core.engine.Filter """
    title = 'Max'
    note = ['all', 'auto_msk', 'auto_snap', 'preview']
    para = {'num':0}
    view = [('slide', (-100,100), '-100', 'num', '+100')]
    
    def run(self, ips, snap, img, para = None):   
        img[:] = snap
        img[img<para['num']] = para['num']
        
class Min(Filter):
    """Min_plg: derived from imagepy.core.engine.Filter """
    title = 'Min'
    note = ['all', 'auto_msk', 'auto_snap', 'preview']
    para = {'num':0}
    view = [('slide', (-100,100), '-100', 'num', '+100')]
    
    def run(self, ips, snap, img, para = None):
        img[:] = snap
        img[img>para['num']] = para['num']
        
class Sqrt(Filter):
    """Sqrt_plg: derived from imagepy.core.engine.Filter """
    title = 'Squre Root'
    note = ['all', 'auto_msk', 'auto_snap', 'preview']
    
    def run(self, ips, snap, img, para = None):
        np.sqrt(snap, out=img)
        
class Garmma(Filter):
    """Garmma_plg: derived from imagepy.core.engine.Filter """
    title = 'Garmma'
    note = ['all', 'auto_msk', 'auto_snap', 'preview', '2float']
    para = {'num':0}
    view = [(float, (-100,100), 2, '0.1', 'num', '10')]
    
    def run(self, ips, snap, img, para = None):
        x1, x2 = ips.range
        img[:] = snap
        img[:] = (img/(x2-x1))**para['num']*(x2-x1)
    
plgs = [Add, Multiply, '-', Max, Min, '-', Sqrt, Garmma]