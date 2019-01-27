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

class Table:
    title = 'TableFilter'
    note = []
    para = None
    'req_sel, req_row, req_col, snap, row_not, row_msk, col_msk, col_not, num_only, preview'
    view = None
    prgs = (None, 1)
    modal = True
    asyn = True

    def __init__(self, tps=None):
        print('simple start')
        self.tps = IPy.get_tps() if tps==None else tps
        self.dialog = None
    
    def progress(self, i, n):
        self.prgs = (i, n)

    def load(self, ips):return True
        
    def preview(self, tps, para):
        self.run(tps, tps.data, tps.snap, para)
        tps.update()

    def show(self):
        if self.view==None:return True
        self.dialog = ParaDialog(IPy.get_twindow(), self.title)
        self.dialog.init_view(self.view, self.para, 'preview' in self.note, modal=self.modal)
        self.dialog.on_help = lambda : IPy.show_md(self.title, DocumentManager.get(self.title))
        self.dialog.set_handle(lambda x:self.preview(self.tps, self.para))
        if self.modal: return self.dialog.ShowModal() == wx.ID_OK
        self.dialog.on_ok = lambda : self.ok(self.tps)
        self.dialog.on_cancel = lambda : self.cancel(self.tps)
        self.dialog.Show()
    
    def run(self, tps, snap, data, para = None):pass
        
    def cancel(self, tps):
        if 'snap' in self.note:
            tps.data[tps.snap.columns] = tps.snap
            tps.update()

    def ok(self, tps, para=None, callafter=None):
        if para == None: para = self.para
        if self.asyn and IPy.uimode() != 'no':
            threading.Thread(target = self.runasyn, 
                    args = (tps, tps.data, tps.snap, para, callafter)).start()
        else: self.runasyn(tps, tps.data, tps.snap, para, callafter)
        win = WidgetsManager.getref('Macros Recorder')
        if win!=None: win.write('{}>{}'.format(self.title, para))

    def runasyn(self,  tps, snap, data, para = None, callback = None):
        TaskManager.add(self)
        start = time()
        self.run(tps, data, snap, para)
        IPy.set_info('%s: cost %.3fs'%(tps.title, time()-start))
        tps.update('shp')
        TaskManager.remove(self)
        if callback!=None:callback()

    def check(self, tps):
        print(self.note)
        if tps == None:
            IPy.alert('no table opened!')
            return False
        if 'req_sel' in self.note:
            print(tps.rowmsk, tps.colmsk)
            if isinstance(tps.rowmsk, slice) and\
             isinstance(tps.colmsk, slice):
                IPy.alert('no selection!')
                return False
        if 'req_row' in self.note:
            print(tps.rowmsk, tps.colmsk)
            if isinstance(tps.rowmsk, slice):
                IPy.alert('need row selection!')
                return False
        if 'req_col' in self.note:
            print(tps.rowmsk, tps.colmsk)
            if isinstance(tps.colmsk, slice):
                IPy.alert('need col selection!')
                return False
        return True
        
    def snapshot(self, tps):
        note = self.note
        if not 'snap' in note: return None
        if 'row_msk' in note:
            rmsk = True
        elif 'row_not' in note:
            rmsk = False
        else: rmsk = None
        if 'col_msk' in note:
            cmsk = True
        elif 'col_not' in note:
            cmsk = False
        else: cmsk = None
        only = 'num_only' in note
        tps.snapshot(rmsk, cmsk, only)

    def start(self, para=None, callback=None):
        #print self.title, para
        if not self.check(self.tps):return
        if not self.load(self.tps):return
        if 'snap' in self.note:self.snapshot(self.tps)
        if para!=None:
            self.ok(self.tps, para, callback)
        elif self.view==None:
            if not self.__class__.show is Table.show:
                if self.show():
                    self.ok(self.tps, para, callback)
            else: self.ok(self.tps, para, callback)
        elif self.modal:
            if self.show():
                self.ok(self.tps, para, callback)
            else:self.cancel(self.tps)
            if not self.dialog is None: self.dialog.Destroy()
        else: self.show()