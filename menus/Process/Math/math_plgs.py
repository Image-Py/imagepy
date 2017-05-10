# -*- coding: utf-8 -*
import numpy as np
from core.engines import Filter

class Add_plg(Filter):
    """Add_plg: derived from core.engines.Filter """
    title = 'Add'
    note = ['all', 'auto_msk', 'auto_snap', 'preview', '2int']
    para = {'num':0}
    view = [('slide', (-100, 100), '-100', 'num', '+100')]
    
    def run(self, ips, snap, img, para = None):
        if para == None: para = self.para
        img[:] = snap
        np.add(img, para['num'], out=img, casting='unsafe')
        
class Multiply_plg(Filter):
    """Multiply_plg: derived from core.engines.Filter """
    title = 'Multiply'
    note = ['all', 'auto_msk', 'auto_snap', 'preview', '2int']
    para = {'num':0}
    view = [(float, (-100,100), 2, '-100', 'num', '+100')]
    
    def run(self, ips, snap, img, para = None):
        if para == None: para = self.para     
        img[:] = snap
        np.multiply(img, para['num'], out=img, casting='unsafe')
        
class Max_plg(Filter):
    """Max_plg: derived from core.engines.Filter """
    title = 'Max'
    note = ['all', 'auto_msk', 'auto_snap', 'preview']
    para = {'num':0}
    view = [('slide', (-100,100), '-100', 'num', '+100')]
    
    def run(self, ips, snap, img, para = None):
        if para == None: para = self.para     
        img[:] = snap
        img[img<para['num']] = para['num']
        
class Min_plg(Filter):
    """Min_plg: derived from core.engines.Filter """
    title = 'Min'
    note = ['all', 'auto_msk', 'auto_snap', 'preview']
    para = {'num':0}
    view = [('slide', (-100,100), '-100', 'num', '+100')]
    
    def run(self, ips, snap, img, para = None):
        if para == None: para = self.para
        img[:] = snap
        img[img>para['num']] = para['num']
        
class Sqrt_plg(Filter):
    """Sqrt_plg: derived from core.engines.Filter """
    title = 'Squre Root'
    note = ['all', 'auto_msk', 'auto_snap', 'preview']
    
    def run(self, ips, snap, img, para = None):
        np.sqrt(snap, out=img)
        
class Garmma_plg(Filter):
    """Garmma_plg: derived from core.engines.Filter """
    title = 'Garmma'
    note = ['all', 'auto_msk', 'auto_snap', 'preview', '2float']
    para = {'num':0}
    view = [(float, (-100,100), 2, '0.1', 'num', '10')]
    
    def run(self, ips, snap, img, para = None):
        x1, x2 = ips.range
        img[:] = snap
        img[:] = (img/(x2-x1))**para['num']*(x2-x1)
    
plgs = [Add_plg, Multiply_plg, 
        '-', Max_plg, Min_plg, 
        '-', Sqrt_plg, Garmma_plg]