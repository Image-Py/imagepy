# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 23:48:33 2016

@author: yxl
"""

from ui.panelconfig import ParaDialog
from core.managers import TextLogManager
import numpy as np
import IPy
import wx
        
def process_chanels(plg, ips, src, des, para):
    if ips.chanels>1 and not 'not_channel' in plg.note:
        for i in range(ips.chanels):
            rst = plg.run(ips, src[:,:,i], des[:,:,i], para)
            if not rst is des and rst!=None:
                des[:,:,i] = rst
    else:
        rst = plg.run(ips, src, des, para)
        if not rst is des and rst!=None:
            des[:] = rst
    return des
    
def process_one(plg, ips, src, img, para):
    transint = '2int' in plg.note and ips.dtype == np.uint8
    transfloat = '2float' in plg.note and not ips.dtype in (np.float32, np.float64)
    if transint: buf =  img.astype(np.int32)
    if transfloat: buf = img.astype(np.float32)
    rst = process_chanels(plg, ips, src, buf if transint or transfloat else img, para)
    if not img is rst and rst != None:
        np.clip(rst, ips.range[0], ips.range[1], out=img)
    if 'auto_msk' in plg.note and ips.get_msk()!=None:
        msk = True-ips.get_msk()
        img[msk] = src[msk]
    return img
    
def process_stack(plg, ips, src, imgs, para):
    from time import time
    start = time()
    transint = '2int' in plg.note and ips.dtype == np.uint8
    transfloat = '2float' in plg.note and not ips.dtype in (np.float32, np.float64)
    if transint: buf =  imgs[0].astype(np.int32)
    if transfloat: buf = imgs[0].astype(np.float32)
    for i,n in zip(imgs,range(len(imgs))):
        IPy.curapp.set_progress(round((n+1)*100.0/len(imgs)))
        src[:] = i
        if transint or transfloat: buf[:] = i
        rst = process_chanels(plg, ips, src, buf if transint or transfloat else i, para)
        if not i is rst and rst != None:
            np.clip(rst, ips.range[0], ips.range[1], out=i)
        if 'auto_msk' in plg.note and ips.get_msk()!=None:
            msk = True - ips.get_msk()
            i[msk] = src[msk]
    IPy.curapp.set_progress(0)
    print time()-start
    return imgs
    
class Filter:
    title = 'Filter'
    note = []
    'all, 8_bit, 16_bit, rgb, float, not_channel, not_slice, req_roi, auto_snap, auto_msk, preview, 2int, 2float'
    para = None
    view = None#[(float, (0,30), 1,  'sigma', 'sigma', 'pix')]
    
    def __init__(self, ips=None):
        if ips==None:ips = IPy.get_ips()
        self.dialog = None
        self.ips = ips
    
    def load(self, ips):return True
        
    def show(self):
        if self.view==None:return wx.ID_OK
        self.dialog = ParaDialog(IPy.get_window(), self.title)
        self.dialog.init_view(self.view, self.para, 'preview' in self.note, modal=True)
        self.dialog.set_handle(lambda x:self.preview(self.para))
        return self.dialog.ShowModal()
    
    def run(self, ips, img, buf, para = None):
        return 255-buf
        
    def check(self, ips):
        note = self.note
        if ips == None:
            IPy.alert('no image opened!')
            return False
        elif 'req_roi' in note and ips.roi == None:
            IPy.alert('no Roi found!')
            return False
        elif not 'all' in note:
            if ips.get_imgtype()=='rgb' and not 'rgb' in note:
                IPy.alert('do not surport rgb image')
                return False
            elif ips.get_imgtype()=='8-bit' and not '8-bit' in note:
                IPy.alert('do not surport 8-bit image')
                return False
            elif ips.get_imgtype()=='16-bit' and not '16-bit' in note:
                IPy.alert('do not surport 16-bit image')
                return False
            elif ips.get_imgtype()=='float' and not 'float' in note:
                IPy.alert('do not surport float image')
                return False
        return True
        
    def preview(self, para):
        process_one(self, self.ips, self.ips.snap, self.ips.get_img(), para)
        self.ips.update = True
        
    def start(self, para=None):
        ips = self.ips
        if not self.check(ips):return
        if not self.load(ips):return
        if 'auto_snap' in self.note:ips.snapshot()
        if para!=None or self.show() == wx.ID_OK:
            if para == None:
                para = self.para
                if not 'not_slice' in self.note and ips.get_nslices()>1:
                    if para == None:para = {}
                if para!=None and para.has_key('stack'):del para['stack']
            win = TextLogManager.get('Recorder')
            if ips.get_nslices()==1 or 'not_slice' in self.note:
                process_one(self, ips, ips.snap, ips.get_img(), para)
                if win!=None: win.append('%s>%s'%(self.title, para))
            elif ips.get_nslices()>1:
                has, rst = para.has_key('stack'), None
                if not has:
                    rst = IPy.yes_no('run every slice in current stacks?')
                if 'auto_snap' in self.note:ips.swap()
                if has and para['stack'] or rst == 'yes':
                    para['stack'] = True
                    process_stack(self, ips, ips.snap, ips.imgs, para)
                    if win!=None: win.append('%s>%s'%(self.title, para))
                elif has and not para['stack'] or rst == 'no': 
                    para['stack'] = False
                    process_one(self, ips, ips.snap, ips.get_img(), para)
                    if win!=None: win.append('%s>%s'%(self.title, para))
                elif rst == 'cancel': pass
            ips.update = True
        else : 
            if 'auto_snap' in self.note:
                ips.swap()
                ips.update = True
        if self.dialog!=None:self.dialog.Destroy()