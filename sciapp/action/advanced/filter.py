# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 23:48:33 2016
@author: yxl
"""

import threading
import numpy as np
from time import time, sleep

def process_channels(plg, ips, src, des, para):
    if ips.channels>1 and not 'not_channel' in plg.note:
        for i in range(ips.channels):
            rst = plg.run(ips, src if src is None else src[:,:,i], des[:,:,i], para)
            if not rst is des and not rst is None:
                des[:,:,i] = rst
    else:
        rst = plg.run(ips, src, des, para)
        if not rst is des and not rst is None:
            des[:] = rst
    return des

def process_one(plg, ips, src, img, para, callafter=None):
    if callafter != 'no record':
        plg.app.record_macros('{}>{}'.format(plg.title, para))
    plg.app.add_task(plg)
    start = time()
    transint = '2int' in plg.note and ips.dtype in (np.uint8, np.uint16)
    transfloat = '2float' in plg.note and not ips.dtype in (np.complex128, np.float32, np.float64)
    if transint: 
        buf = img.astype(np.int32)
        src = src.astype(np.int32)
    if transfloat: 
        buf = img.astype(np.float32)
        src = src.astype(np.float32)
    rst = process_channels(plg, ips, src, buf if transint or transfloat else img, para)
    if not img is rst and not rst is None:
        imgrange = {np.uint8:(0,255), np.uint16:(0, 65535)}[img.dtype.type]
        np.clip(rst, imgrange[0], imgrange[1], out=img)
    if 'auto_msk' in plg.note and not ips.mask('out') is None:
        msk = ips.mask('out')
        img[msk] = src[msk]
    plg.app.info('%s: cost %.3fs'%(plg.title, time()-start))
    ips.update()
    plg.app.remove_task(plg)
    if not callafter in (None, 'no record'):callafter()
    
def process_stack(plg, ips, src, imgs, para, callafter=None):
    plg.app.record_macros('{}>{}'.format(plg.title, para))
    plg.app.add_task(plg)
    start = time()
    transint = '2int' in plg.note and ips.dtype in (np.uint8, np.uint16)
    transfloat = '2float' in plg.note and not ips.dtype in (np.complex128, np.float32, np.float64)
    if transint: 
        buf =  imgs[0].astype(np.int32)
        src = src.astype(np.int32)
    elif transfloat: 
        buf = imgs[0].astype(np.float32)
        src = src.astype(np.float32)
    else: src = src * 1

    for i,n in zip(imgs,list(range(len(imgs)))):
        #sleep(0.5)
        plg.progress(n+1, len(imgs))
        if 'auto_snap' in plg.note : src[:] = i
        if transint or transfloat: buf[:] = i
        rst = process_channels(plg, ips, src, buf if transint or transfloat else i, para)
        if not i is rst and not rst is None:
            imgrange = {np.uint8:(0,255), np.uint16:(0,65535)}[i.dtype.type]
            np.clip(rst, imgrange[0], imgrange[1], out=i)
        if 'auto_msk' in plg.note and not ips.mask() is None:
            msk = ips.mask('out')
            i[msk] = src[msk]
    plg.app.info('%s: cost %.3fs'%(ips.title, time()-start))
    ips.update()
    plg.app.remove_task(plg)
    if not callafter is None:callafter()
    

class Filter:
    title = 'Filter'
    modal = True
    asyn = True
    note = []
    'all, 8-bit, 16-bit, int, rgb, float, not_channel, not_slice, req_roi, auto_snap, auto_msk, preview, 2int, 2float'
    para = None
    view = None
    prgs = None

    def __init__(self, ips=None): pass
        
    def progress(self, i, n): self.prgs = int(i*100/n)

    def show(self):
        preview = lambda para, ips=self.ips: self.preview(ips, para) or ips.update()
        return self.app.show_para(self.title, self.para, self.view, preview, 
            on_ok=lambda : self.ok(self.ips), on_help=self.on_help,
            on_cancel=lambda : self.cancel(self.ips) or self.ips.update(), 
            preview='preview' in self.note, modal=self.modal)
    
    def run(self, ips, snap, img, para = None):
        return 255-img
        
    def check(self, ips):
        note = self.note
        if ips == None:
            return self.app.alert('No image opened!')
            return False
        elif 'req_roi' in note and ips.roi == None:
            return self.app.alert('No Roi found!')
        elif not 'all' in note:
            if ips.dtype==np.uint8 and ips.channels==3 and not 'rgb' in note:
                return self.app.alert('Do not surport rgb image')
            elif ips.dtype==np.uint8 and ips.channels==1 and not '8-bit' in note:
                return self.app.alert('Do not surport 8-bit image')
            elif ips.dtype==np.uint16 and not '16-bit' in note:
                return self.app.alert('Do not surport 16-bit uint image')
            elif ips.dtype in [np.int32, np.int64] and not 'int' in note:
                return self.app.alert('Do not surport int image')
            elif ips.dtype in [np.float32, np.float64] and not 'float' in note:
                return self.app.alert('Do not surport float image')
        return True
        
    def preview(self, ips, para):
        process_one(self, ips, ips.snap, ips.img, para, 'no record')
        
    def load(self, ips):return True
          
    def ok(self, ips, para=None, callafter=None):
        if para == None:
            para = self.para
            if not 'not_slice' in self.note and ips.slices>1:
                if para == None:para = {}
            if para!=None and 'stack' in para:del para['stack']
        # = WidgetsManager.getref('Macros Recorder')
        if ips.slices==1 or 'not_slice' in self.note:
            # process_one(self, ips, ips.snap, ips.img, para)
            if self.asyn and self.app.asyn:
                threading.Thread(target = process_one, args = 
                    (self, ips, ips.snap, ips.img, para, callafter)).start()
            else: process_one(self, ips, ips.snap, ips.img, para, callafter)
            # if win!=None: win.write('{}>{}'.format(self.title, para))
            
        elif ips.slices>1:
            has, rst = 'stack' in para, None
            if not has:
                rst = self.app.yes_no('Run every slice in current stacks?')
            if 'auto_snap' in self.note and self.modal:ips.img[:] = ips.snap
            if has and para['stack'] or rst == 'yes':
                para['stack'] = True
                #process_stack(self, ips, ips.snap, ips.imgs, para)
                if self.asyn and self.app.asyn:
                    threading.Thread(target = process_stack, args = 
                        (self, ips, ips.snap, ips.imgs, para, callafter)).start()
                else: process_stack(self, ips, ips.snap, ips.imgs, para, callafter)
                
            elif has and not para['stack'] or rst == 'no': 
                para['stack'] = False
                #process_one(self, ips, ips.snap, ips.img, para)
                if self.asyn and self.app.asyn:
                    threading.Thread(target = process_one, args = 
                        (self, ips, ips.snap, ips.img, para, callafter)).start()
                else: process_one(self, ips, ips.snap, ips.img, para, callafter)
            elif rst == 'cancel': pass
        #ips.update()
        
    def on_help(self):
        self.app.show_md(self.__doc__ or 'No Document!', self.title)

    def cancel(self, ips):
        if 'auto_snap' in self.note:
            ips.img[:] = ips.snap
            ips.update()
            
    def start(self, app, para=None, callafter=None):
        self.app, self.ips = app, app.get_img()
        if not self.check(self.ips):return
        if not self.load(self.ips):return
        if 'auto_snap' in self.note:self.ips.snapshot()
        
        if para!=None:
            self.ok(self.ips, para, callafter)
        elif self.view==None:
            if not self.__class__.show is Filter.show:
                if self.show():
                    self.ok(self.ips, para, callafter)
            else: self.ok(self.ips, para, callafter)
        elif self.modal:
            if self.show():
                self.ok(self.ips, None, callafter)
            else:self.cancel(self.ips)
        else: self.show()

    def __del__(self):
        print('filter del')
