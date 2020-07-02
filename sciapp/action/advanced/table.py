# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 03:32:05 2016
@author: yxl
"""
import threading
from time import time

class Table:
    title = 'TableFilter'
    note = []
    para = None
    'req_sel, req_row, req_col, auto_snap, auto_msk, msk_not, num_only, preview'
    view = None
    prgs = None
    modal = True
    asyn = True

    def __init__(self, tps=None):
        
        self.dialog = None
    
    def progress(self, i, n): self.prgs = int(i*100/n)

    def load(self, tps):return True
        
    def preview(self, tps, para):
        self.run(tps, tps.snap, tps.data, para)
        tps.update()
    
    def show(self):
        preview = lambda para, tps=self.tps: self.preview(tps, para) or tps.update()
        return self.app.show_para(self.title, self.para, self.view, preview, 
            on_ok=lambda : self.ok(self.tps), on_help=self.on_help,
            on_cancel=lambda : self.cancel(self.tps) or self.tps.update(), 
            preview='preview' in self.note, modal=self.modal)
    
    def run(self, tps, snap, data, para = None):pass
        
    def cancel(self, tps):
        if 'auto_snap' in self.note:
            tps.data[tps.snap.columns] = tps.snap
            tps.update()

    def on_help(self):
        self.app.show_md(self.__doc__ or 'No Document!', self.title)

    def ok(self, tps, para=None, callafter=None):
        if para == None: para = self.para
        if self.asyn and self.app.asyn:
            threading.Thread(target = self.runasyn, 
                args = (tps, tps.data, tps.snap, para, callafter)).start()
        else: self.runasyn(tps, tps.data, tps.snap, para, callafter)

    def runasyn(self,  tps, snap, data, para = None, callback = None):
        self.app.record_macros('{}>{}'.format(self.title, para))
        self.app.add_task(self)
        start = time()
        self.run(tps, data, snap, para)
        self.app.info('%s: cost %.3fs'%(tps.title, time()-start))
        tps.update()
        self.app.remove_task(self)
        if callback!=None:callback()

    def check(self, tps):
        print(self.note)
        if tps == None:
            self.app.alert('no table opened!')
            return False
        if 'req_sel' in self.note:
            print(tps.rowmsk, tps.colmsk)
            if isinstance(tps.rowmsk, slice) and\
             isinstance(tps.colmsk, slice):
                self.app.alert('no selection!')
                return False
        if 'req_row' in self.note:
            print(tps.rowmsk, tps.colmsk)
            if isinstance(tps.rowmsk, slice):
                self.app.alert('need row selection!')
                return False
        if 'req_col' in self.note:
            print(tps.rowmsk, tps.colmsk)
            if isinstance(tps.colmsk, slice):
                self.app.alert('need col selection!')
                return False
        return True

    def start(self, app, para=None, callback=None):
        self.app, self.tps = app, app.get_table()
        #print self.title, para
        if not self.check(self.tps):return
        if not self.load(self.tps):return
        if 'auto_snap' in self.note:
            if 'auto_msk' in self.note: mode = True
            elif 'msk_not' in self.note: mode = False
            else: mode = None
            self.tps.snapshot(mode, 'num_only' in self.note)
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