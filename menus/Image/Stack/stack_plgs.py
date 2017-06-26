# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 11:26:12 2016
@author: yxl
"""
from imagepy.core.engine import Simple
class SetSlice(Simple):
    title = 'Set Slice'
    note = ['all']
    
    #parameter
    para = {'num':0}
    view = [(int, (0,999), 0, 'Num', 'num', '')]

    #process
    def run(self, ips, imgs, para = None):
        if para['num']>=0 and para['num']<ips.get_nslices():
            ips.set_cur(para['num'])
        
class Next(Simple):
    title = 'Next Slice'
    note = ['all']

    #process
    def run(self, ips, imgs, para = None):
        if ips.cur<ips.get_nslices()-1:
            ips.cur+=1
            
class Pre(Simple):
    title = 'Previous Slice'
    note = ['all']

    #process
    def run(self, ips, imgs, para = None):
        if ips.cur>0:
            ips.cur-=1
            
class Delete(Simple):
    title = 'Delete Slice'
    note = ['stack', 'all']

    #process
    def run(self, ips, imgs, para = None):
        ips.imgs.pop(ips.cur)
        if ips.cur==ips.get_nslices():
            ips.cur -= 1
            
class Add(Simple):
    title = 'Add Slice'
    note = ['all']

    #process
    def run(self, ips, imgs, para = None):
        ips.imgs.insert(ips.cur, ips.img*0)
            
plgs = [SetSlice, Next, Pre, Add, Delete]