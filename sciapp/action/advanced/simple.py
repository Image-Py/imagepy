# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 03:32:05 2016
@author: yxl
"""
import threading
from time import time
import numpy as np

class Simple:
    title = 'SimpleFilter'
    asyn = True
    note = []
    para = None
    'all, 8-bit, 16-bit, rgb, float, req_roi, stack, stack2d, stack3d, preview'
    view = None
    prgs = None
    modal = True

    def __init__(self): pass

    def load(self, ips):return True
        
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
            elif ips.dtype==np.int32 and not 'int' in note:
                self.app.alert('Do not surport 32-bit int uint image')
                return False
            elif (ips.dtype==np.float32 or ips.dtype==np.float64) and not 'float' in note:
                self.app.alert('Do not surport float image')
                return False
        if sum([i in note for i in ('stack','stack2d','stack3d')])>0:
            if ips.slices==1:
                self.app.alert('Stack required!')
                return False
            elif 'stack2d' in note and ips.isarray:
                self.app.alert('Stack2d required!')
                return False
            elif 'stack3d' in note and not ips.isarray:
                self.app.alert('Stack3d required!')
                return False
        return True

    def preview(self, ips, para):pass

    def progress(self, i, n): self.prgs = int(i*100/n)

    def show(self):
        preview = lambda para, ips=self.ips: self.preview(ips, para) or ips.update()
        return self.app.show_para(self.title, self.para, self.view, preview, 
            on_ok=lambda : self.ok(self.ips), on_help=self.on_help,
            on_cancel=lambda : self.cancel(self.ips) or self.ips.update(), 
            preview='preview' in self.note, modal=self.modal)
    
    def run(self, ips, imgs, para = None):pass

    def cancel(self, ips):pass

    def on_help(self):
        self.app.show_md(self.__doc__ or 'No Document!', self.title)

    def ok(self, ips, para=None, callafter=None):
        if para == None: para = self.para
        if self.asyn and self.app.asyn:
            threading.Thread(target = self.runasyn, 
                    args = (ips, ips.imgs, para, callafter)).start()
        else: self.runasyn(ips, ips.imgs, para, callafter)

    def runasyn(self,  ips, imgs, para = None, callback = None):
        self.app.record_macros('{}>{}'.format(self.title, para))
        self.app.add_task(self)
        start = time()
        self.run(ips, imgs, para)
        self.app.info('%s: cost %.3fs'%(self.title, time()-start))
        ips.update()
        self.app.remove_task(self)
        if callback!=None:callback()
        
    def start(self, app, para=None, callback=None):
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