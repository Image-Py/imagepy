# -*- coding: utf-8 -*
import numpy as np
from sciapp.action import Filter

class Add(Filter):
    """Add_plg: derived from sciapp.action.Filter """
    title = 'Add'
    note = ['all', 'auto_msk', 'auto_snap', 'preview', '2int']
    para = {'num':0}
    view = [('slide', 'num', (-255, 255), 2, 'value')]
    
    def run(self, ips, snap, img, para = None):
        np.add(snap, para['num'], out=img, casting='unsafe')

class Subtract(Filter):
    """Subtract_plg: derived from sciapp.action.Filter """
    title = 'Subtract'
    note = ['all', 'auto_msk', 'auto_snap', 'preview', '2int']
    para = {'num':0}
    view = [(float, 'num', (-255,255), 2, '-255', '+255')]
    
    def run(self, ips, snap, img, para = None):
        np.subtract(snap, para['num'], out=img, casting='unsafe')

class Multiply(Filter):
    """Multiply_plg: derived from sciapp.action.Filter """
    title = 'Multiply'
    note = ['all', 'auto_msk', 'auto_snap', 'preview', '2int']
    para = {'num':0}
    view = [(float, 'num', (-255,255), 2, '-100', '+100')]
    
    def run(self, ips, snap, img, para = None):
        np.multiply(snap, para['num'], out=img, casting='unsafe')
        
class Max(Filter):
    """Max_plg: derived from sciapp.action.Filter """
    title = 'Max'
    note = ['all', 'auto_msk', 'auto_snap', 'preview']
    para = {'num':0}
    view = [('slide', 'num', (-255,255), 2, '-100')]
    
    def run(self, ips, snap, img, para = None):   
        img[:] = snap
        img[img<para['num']] = para['num']
        
class Min(Filter):
    """Min_plg: derived from sciapp.action.Filter """
    title = 'Min'
    note = ['all', 'auto_msk', 'auto_snap', 'preview']
    para = {'num':0}
    view = [('slide', 'num', (-255,255), 2, '-100')]
    
    def run(self, ips, snap, img, para = None):
        img[:] = snap
        img[img>para['num']] = para['num']
         

class Sqrt(Filter):
    """Sqrt_plg: derived from sciapp.action.Filter """
    title = 'Square Root'
    note = ['all', 'auto_msk', 'auto_snap', 'preview']
    
    def run(self, ips, snap, img, para = None):
        np.sqrt(snap, out=img, casting='unsafe')
        
class Gamma(Filter):
    """Garmma_plg: derived from sciapp.action.Filter """
    title = 'Gamma'
    note = ['all', 'auto_msk', 'auto_snap', 'preview', '2float']
    para = {'num':0}
    view = [(float, 'num', (-255,255), 2, '0.1', '10')]
    
    def run(self, ips, snap, img, para = None):
        x1, x2 = ips.range
        img[:] = snap
        img[:] = (img/(x2-x1))**para['num']*(x2-x1)
    
plgs = [Add, Subtract, Multiply, '-', Max, Min, '-', Sqrt, Gamma]