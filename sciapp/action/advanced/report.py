# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 01:48:23 2016
@author: yxl
"""
import wx
from sciapp import app
from sciapp.action.advanced.dataio import ReaderManager
# from imagepy.core.manager import ReaderManager, ViewerManager
from sciwx.widgets.propertygrid import GridDialog
from sciapp.util import xlreport
from time import time
import openpyxl as pyxl

class Report:
    def __init__(self, title, cont):
        self.title = title
        self.cont = cont
        
    def __call__(self): return self

    def runasyn(self,  wb, info, key, para = None, callback = None):
        self.app.add_task(self)
        for i in para: 
            if i in key and key[i][0] == 'img':
                ips = self.app.get_img(para[i])
                para[i] = ips if ips is None else ips.img

            if i in key and key[i][0] == 'tab':
                tps = self.app.get_table(para[i])
                para[i] = tps if tps is None else tps.data

        start = time()
        xlreport.fill_value(wb, info, para)
        wb.save(para['path'])
        self.app.info('%s: cost %.3fs'%(self.title, time()-start))
        self.app.remove_task(self)
        if callback!=None:callback()

    def start(self, app, para=None, callafter=None):
        self.app = app
        wb = pyxl.load_workbook(self.cont)
        xlreport.repair(wb)
        info, key = xlreport.parse(wb)

        if para is not None: 
            return self.runasyn(wb, info, para, callafter)
        dialog = GridDialog(self.app, self.title, info, key)
        rst = dialog.ShowModal()
        para = dialog.GetValue()

        dialog.Destroy()
        if rst != 5100: return
        filt = ['XLSX', 'xlsx', 'xlsx']
        path = self.app.get_path('Save..', filt, 'save')
        if not path: return
        para['path'] = path 
        self.app.record_macros('{}>{}'.format(self.title, para))
        self.runasyn(wb, info, key, para, callafter)

def show_rpt(data, title):
    wx.CallAfter(Report(title, data).start)
    
# ViewerManager.add('rpt', show_rpt)
def read_rpt(path): return path
ReaderManager.add('rpt', read_rpt, tag='rpt')