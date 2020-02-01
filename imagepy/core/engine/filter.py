# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 23:48:33 2016
@author: yxl
"""

import wx
import threading
import numpy as np

from ... import IPy
from ...ui.panelconfig import ParaDialog
from ...core.manager import TextLogManager, ImageManager, \
WindowsManager, TaskManager, WidgetsManager, DocumentManager
from time import time

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
    TaskManager.add(plg)
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
    if 'auto_msk' in plg.note and not ips.get_msk() is None:
        msk = True ^ ips.get_msk()
        img[msk] = src[msk]
    IPy.set_info('%s: cost %.3fs'%(ips.title, time()-start))
    ips.update()
    TaskManager.remove(plg)
    if not callafter is None:callafter()
    
def process_stack(plg, ips, src, imgs, para, callafter=None):
    TaskManager.add(plg)
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
        plg.progress(n, len(imgs))
        if 'auto_snap' in plg.note : src[:] = i
        if transint or transfloat: buf[:] = i
        rst = process_channels(plg, ips, src, buf if transint or transfloat else i, para)
        if not i is rst and not rst is None:
            imgrange = {np.uint8:(0,255), np.uint16:(0,65535)}[i.dtype.type]
            np.clip(rst, imgrange[0], imgrange[1], out=i)
        if 'auto_msk' in plg.note and not ips.get_msk() is None:
            msk = True ^ ips.get_msk()
            i[msk] = src[msk]
    IPy.set_info('%s: cost %.3fs'%(ips.title, time()-start))
    ips.update()
    TaskManager.remove(plg)
    if not callafter is None:callafter()
    

class Filter:
    title = 'Filter'
    modal = True
    note = []
    'all, 8-bit, 16-bit, int, rgb, float, not_channel, not_slice, req_roi, auto_snap, auto_msk, preview, 2int, 2float'
    para = None
    view = None
    prgs = (None, 1)

    def __init__(self, ips=None):
        if ips==None:ips = IPy.get_ips()
        self.dialog = None
        self.ips = ips
        
    def progress(self, i, n):
        self.prgs = (i, n)

    def show(self, temp=ParaDialog):
        self.dialog = temp(WindowsManager.get(), self.title)
        self.dialog.init_view(self.view, self.para, 'preview' in self.note, modal=self.modal)

        self.dialog.on_help = lambda : IPy.show_md(self.title, DocumentManager.get(self.title))
        self.dialog.set_handle(lambda x:self.preview(self.ips, x))

        self.dialog.on_ok = lambda : self.ok(self.ips)
        self.dialog.on_cancel = lambda : self.cancel(self.ips)
        if self.modal: return self.dialog.ShowModal() == wx.ID_OK
        self.dialog.Show()
    
    def run(self, ips, snap, img, para = None):
        return 255-img
        
    def check(self, ips):
        note = self.note
        if ips == None:
            IPy.alert('No image opened!')
            return False
        elif 'req_roi' in note and ips.roi == None:
            IPy.alert('No Roi found!')
            return False
        elif not 'all' in note:
            if ips.get_imgtype()=='rgb' and not 'rgb' in note:
                IPy.alert('Do not surport rgb image')
                return False
            elif ips.get_imgtype()=='8-bit' and not '8-bit' in note:
                IPy.alert('Do not surport 8-bit image')
                return False
            elif ips.get_imgtype()=='16-bit' and not '16-bit' in note:
                IPy.alert('Do not surport 16-bit uint image')
                return False
            elif ips.get_imgtype()=='32-int' and not 'int' in note:
                IPy.alert('Do not surport 32-bit int uint image')
                return False
            elif 'float' in ips.get_imgtype() and not 'float' in note:
                IPy.alert('Do not surport float image')
                return False
        return True
        
    def preview(self, ips, para):
        process_one(self, ips, ips.snap, ips.img, para, None)
        
    def load(self, ips):return True
          
    def ok(self, ips, para=None, callafter=None):
        if para == None:
            para = self.para
            if not 'not_slice' in self.note and ips.get_nslices()>1:
                if para == None:para = {}
            if para!=None and 'stack' in para:del para['stack']
        win = WidgetsManager.getref('Macros Recorder')
        if ips.get_nslices()==1 or 'not_slice' in self.note:
            # process_one(self, ips, ips.snap, ips.img, para)
            if IPy.uimode() == 'no':
                process_one(self, ips, ips.snap, ips.img, para, callafter)
            else: threading.Thread(target = process_one, args = 
                (self, ips, ips.snap, ips.img, para, callafter)).start()
            if win!=None: win.write('{}>{}'.format(self.title, para))
        elif ips.get_nslices()>1:
            has, rst = 'stack' in para, None
            if not has:
                rst = IPy.yes_no('Run every slice in current stacks?')
            if 'auto_snap' in self.note and self.modal:ips.reset()
            if has and para['stack'] or rst == 'yes':
                para['stack'] = True
                #process_stack(self, ips, ips.snap, ips.imgs, para)
                if IPy.uimode() == 'no':
                    process_stack(self, ips, ips.snap, ips.imgs, para, callafter)
                else: threading.Thread(target = process_stack, args = 
                    (self, ips, ips.snap, ips.imgs, para, callafter)).start()
                if win!=None: win.write('{}>{}'.format(self.title, para))
            elif has and not para['stack'] or rst == 'no': 
                para['stack'] = False
                #process_one(self, ips, ips.snap, ips.img, para)
                if IPy.uimode() == 'no':
                    process_one(self, ips, ips.snap, ips.img, para, callafter)
                else: threading.Thread(target = process_one, args = 
                    (self, ips, ips.snap, ips.img, para, callafter)).start()
                if win!=None: win.write('{}>{}'.format(self.title, para))
            elif rst == 'cancel': pass
        #ips.update()
        
    def cancel(self, ips):
        if 'auto_snap' in self.note:
            ips.img[:] = ips.snap
            ips.update()
            
    def start(self, para=None, callafter=None):
        ips = self.ips
        if not self.check(ips):return
        if not self.load(ips):return
        if 'auto_snap' in self.note:ips.snapshot()
        
        if para!=None:
            self.ok(self.ips, para, callafter)
        elif self.view==None:
            if not self.__class__.show is Filter.show:
                if self.show():
                    self.ok(self.ips, para, callafter)
            else: self.ok(self.ips, para, callafter)
        elif self.modal:
            if self.show():
                self.ok(ips, None, callafter)
            else:self.cancel(ips)
            self.dialog.Destroy()
        else: self.show()

    def __del__(self):
        print('filter del')