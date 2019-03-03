# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 03:32:05 2016
@author: yxl
"""
import wx
import threading

from ... import IPy
from ...ui.panelconfig import ParaDialog
from ..manager import TextLogManager, TaskManager, WidgetsManager, DocumentManager
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

    def __init__(self, ips=None):
        print('Simple start')
        self.ips = IPy.get_ips() if ips==None else ips
        self.dialog = None
    
    def progress(self, i, n):
        self.prgs = (i, n)

    def load(self, ips):return True
        
    def preview(self, ips, para):pass

    def show(self, temp=ParaDialog):
        if self.view==None:return True
        self.dialog = temp(IPy.get_window(), self.title)
        self.dialog.init_view(self.view, self.para, 'preview' in self.note, modal=self.modal)
        self.dialog.on_help = lambda : IPy.show_md(self.title, DocumentManager.get(self.title))
        self.dialog.set_handle(lambda x:self.preview(self.ips, self.para) is self.ips.update())
        if self.modal: return self.dialog.ShowModal() == wx.ID_OK
        self.dialog.on_ok = lambda : self.ok(self.ips)
        self.dialog.on_cancel = lambda : self.cancel(self.ips) is self.ips.update()
        self.dialog.Show()
    
    def run(self, ips, imgs, para = None):pass
        
    def cancel(self, ips):pass

    def ok(self, ips, para=None, callafter=None):
        if para == None: para = self.para
        if self.asyn and IPy.uimode()!='no':
            threading.Thread(target = self.runasyn, 
                    args = (ips, ips.imgs, para, callafter)).start()
        else: self.runasyn(ips, ips.imgs, para, callafter)
        win = WidgetsManager.getref('Macros Recorder')
        if win!=None: win.write('{}>{}'.format(self.title, para))

    def runasyn(self,  ips, imgs, para = None, callback = None):
        TaskManager.add(self)
        start = time()
        self.run(ips, imgs, para)
        IPy.set_info('%s: cost %.3fs'%(ips.title, time()-start))
        ips.update()
        TaskManager.remove(self)
        if callback!=None:callback()

    def check(self, ips):
        note = self.note
        if ips == None:
            IPy.alert('No image opened!')
            return False
        if 'req_roi' in note and ips.roi == None:
            IPy.alert('No Roi found!')
            return False
        if not 'all' in note:
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
        if sum([i in note for i in ('stack','stack2d','stack3d')])>0:
            if ips.get_nslices()==1:
                IPy.alert('Stack required!')
                return False
            elif 'stack2d' in note and ips.is3d:
                IPy.alert('Stack2d required!')
                return False
            elif 'stack3d' in note and not ips.is3d:
                IPy.alert('Stack3d required!')
                return False
        return True
        
    def start(self, para=None, callback=None):
        #print self.title, para
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
            if not self.dialog is None: self.dialog.Destroy()
        else: self.show()