# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 03:32:05 2016
@author: yxl
"""
import wx
import threading
import numpy as np
from time import time

class Simple:
    title = 'SimpleFilter'
    asyn = True
    note = []
    para = None
    'all, 8-bit, 16-bit, rgb, float, req_roi, stack, stack2d, stack3d, preview'
    view = None
    prgs = (None, 1)
    modal = True

    def __init__(self): pass
    
    def progress(self, i, n):
        self.prgs = (i, n)

    def load(self, ips):return True
        
    def preview(self, ips, para):pass

    def show(self):
        preview = lambda para, ips=self.ips: self.preview(ips, para) or ips.update()
        return self.app.show_para(self.title, self.view, self.para, preview, 
            on_ok=lambda : self.ok(self.ips), on_cancel=lambda : self.cancel(self.ips) or self.ips.update(), 
            preview='preview' in self.note, modal=self.modal)
    
    def run(self, ips, imgs, para = None):pass
        
    def cancel(self, ips):pass

    def ok(self, ips, para=None, callafter=None):
        if para == None: para = self.para
        if self.asyn :
            threading.Thread(target = self.runasyn, 
                    args = (ips, ips.imgs, para, callafter)).start()
        else: self.runasyn(ips, ips.imgs, para, callafter)

    def runasyn(self,  ips, imgs, para = None, callback = None):
        start = time()
        self.run(ips, imgs, para)
        self.app.info('%s: cost %.3fs'%(ips.title, time()-start))
        ips.update()
        if callback!=None:callback()

    def check(self, ips):
        note = self.note
        if ips == None:
            self.app.alert('No image opened!')
            return False
        if 'req_roi' in note and ips.roi == None:
            self.app.alert('No Roi found!')
            return False
        if not 'all' in note:
            if ips.dtype==np.uint8 and ips.channels==3 and not 'rgb' in note:
                self.app.alert('Do not surport rgb image')
                return False
            elif ips.dtype==np.uint8 and ips.channels==1 and not '8-bit' in note:
                self.app.alert('Do not surport 8-bit image')
                return False
            elif ips.dtype==np.uint16 and not '16-bit' in note:
                self.app.alert('Do not surport 16-bit uint image')
                return False
            elif ips.dtype in [np.int32, np.int64] and not 'int' in note:
                self.app.alert('Do not surport 32-bit int uint image')
                return False
            elif ips.dtype in [np.float32, np.float64] and not 'float' in note:
                self.app.alert('Do not surport float image')
                return False
        if sum([i in note for i in ('stack','stack2d','stack3d')])>0:
            if ips.get_nslices()==1:
                self.app.alert('Stack required!')
                return False
            elif 'stack2d' in note and ips.is3d:
                self.app.alert('Stack2d required!')
                return False
            elif 'stack3d' in note and not ips.is3d:
                self.app.alert('Stack3d required!')
                return False
        return True
        
    def start(self, app, para=None, callback=None):
        #print self.title, para
        self.app, self.ips = app, app.get_img()
        if not self.check(self.ips):return
        if not self.load(self.ips):return

        if para!=None:
            self.ok(self.ips, para, callback)
        elif self.view==None:
            if not self.__class__.show is Simple.show:
                if self.show():
                    self.ok(self.ips, para, callback)
            else: self.ok(self.ips, para, callback)
        elif self.modal:
            if self.show():
                self.ok(self.ips, para, callback)
            else:
                self.cancel(self.ips)
                self.ips.update()
        else: self.show()