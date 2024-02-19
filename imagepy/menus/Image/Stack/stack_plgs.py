# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 11:26:12 2016
@author: yxl
"""
from sciapp.action import Simple

class SetSlice(Simple):
    title = 'Set Slice'
    note = ['all']
    
    #parameter
    para = {'num':0}

    def load(self, ips):
        self.view = [(int, 'num', (0, ips.slices-1), 0, 'Num', '0~%d'%(ips.slices-1))]
        return True
    #process
    def run(self, ips, imgs, para = None):
        if para['num']>=0 and para['num']<ips.slices:
            ips.cur = para['num']
        
class Next(Simple):
    title = 'Next Slice'
    note = ['all']

    #process
    def run(self, ips, imgs, para = None):
        if ips.cur<ips.slices-1: ips.cur+=1
            
class Pre(Simple):
    title = 'Previous Slice'
    note = ['all']

    #process
    def run(self, ips, imgs, para = None):
        if ips.cur>0: ips.cur-=1
            
class Delete(Simple):
    title = 'Delete Slice'
    note = ['stack', 'all']

    #process
    def run(self, ips, imgs, para = None):
        ips.imgs.pop(ips.cur)
        if ips.cur==ips.slices: ips.cur -= 1
            
class Add(Simple):
    title = 'Add Slice'
    note = ['all']

    #process
    def run(self, ips, imgs, para = None):
        ips.imgs.insert(ips.cur, ips.img*0)
            
class Sub(Simple):
    title = 'Sub Stack'
    modal = False
    note = ['all']

    para = {'start':0, 'end':10}


    view = [(int, 'start', (0,1e8), 0, 'start', 'slice'),
            (int, 'end', (0,1e8), 0, 'end', 'slice')]

    def load(self, ips):
        self.view = [(int, 'start', (0,ips.slices-1), 0, 'start', '0~%d'%(ips.slices-1)),
                     (int, 'end', (0,ips.slices-1), 0, 'end', '0~%d'%(ips.slices-1))]
        return True

    def run(self, ips, imgs, para = None):
        s, e = para['start'], para['end']
        self.app.show_img(ips.subimg()[s:e], ips.title+'-substack')

plgs = [SetSlice, Next, Pre, Add, Delete, '-', Sub]