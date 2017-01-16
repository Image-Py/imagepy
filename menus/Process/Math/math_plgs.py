# -*- coding: utf-8 -*
import numpy as np
from core.engines import Filter

class Add_plg(Filter):
    title = 'Add'
    note = ['all', 'auto_msk', 'auto_snap', 'preview', '2int']
    
    #parameter
    para = {'num':0}
    view = [('slide', (-100, 100), '-100', 'num', '+100')]
    #process
    def run(self, ips, scr, des, para = None):
        if para == None: para = self.para
        des[:] = scr        
        des += para['num']
        return des
        
class Multiply_plg(Filter):
    title = 'Multiply'
    note = ['all', 'auto_msk', 'auto_snap', 'preview', '2int']
    
    #parameter
    para = {'num':0}
    view = [(float, (-100,100), 2, '-100', 'num', '+100')]
    #process
    def run(self, ips, scr, des, para = None):
        if para == None: para = self.para
        des[:] = scr         
        des *= para['num']
        return des
        
class Max_plg(Filter):
    title = 'Max'
    note = ['all', 'auto_msk', 'auto_snap', 'preview']
    
    #parameter
    para = {'num':0}
    view = [('slide', (-100,100), '-100', 'num', '+100')]
    #process
    def run(self, ips, scr, des, para = None):
        if para == None: para = self.para
        des[:] = scr         
        des[des<para['num']] = para['num']
        return des
        
class Min_plg(Filter):
    title = 'Min'
    note = ['all', 'auto_msk', 'auto_snap', 'preview']
    
    #parameter
    para = {'num':0}
    view = [('slide', (-100,100), '-100', 'num', '+100')]
    #process
    def run(self, ips, scr, des, para = None):
        if para == None: para = self.para
        des[:] = scr         
        des[des>para['num']] = para['num']
        return des
        
class Sqrt_plg(Filter):
    title = 'Squre Root'
    note = ['all', 'auto_msk', 'auto_snap', 'preview']

    #process
    def run(self, ips, scr, des, para = None):
        np.sqrt(scr, out=des)
        return des
        
class Garmma_plg(Filter):
    title = 'Garmma'
    note = ['all', 'auto_msk', 'auto_snap', 'preview', '2float']

    para = {'num':0}
    view = [(float, (-100,100), 2, '0.1', 'num', '10')]
    #process
    def run(self, ips, scr, des, para = None):
        x1, x2 = ips.range
        des[:] = scr
        des[:] = (des/(x2-x1))**para['num']*(x2-x1)
        return des
    
plgs = [Add_plg, Multiply_plg, '-', Max_plg, Min_plg, '-', Sqrt_plg, Garmma_plg]